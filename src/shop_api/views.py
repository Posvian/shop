import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    DjangoModelPermissions,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from authapp.models import CustomUser
from mainapp.models import Product, Feedback, Cart, CartItem, Order, ProductInOrder
from shop_api.filters import ProductFilter
from shop_api.pagination import FiveResultsSetPagination
from shop_api.permissions import IsOwnerOrReadOnly
from shop_api.serializers import (
    CustomUserSerializer,
    AddProductSerializer,
    FeedbackSerializer,
    CartSerializer,
    OrderSerializer,
)
from shop_api.services import delete_cache
from shop_api.services import (
    get_cart_instance,
    check_cart_products_out_of_stock,
    inform_user_that_products_out_of_stock,
    create_order,
)

logger = logging.getLogger("main")


class CustomUserViewSet(viewsets.ModelViewSet):
    logger.info("Open users list")
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = AddProductSerializer
    pagination_class = FiveResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = ProductFilter
    permission_classes = [
        IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,
        DjangoModelPermissions,
    ]
    # permission_classes = [IsAuthenticated]

    CACHE_KEY_PREFIX = "products-view"

    @method_decorator(cache_page(60 * 10, key_prefix=CACHE_KEY_PREFIX))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        delete_cache(self.CACHE_KEY_PREFIX)
        return response

    @action(methods=["get", "post"], detail=True)
    def review(self, request, pk=None):
        if request.method == "GET":
            reviews = Feedback.objects.filter(product_id=pk).values(
                "user", "feedback", "rating"
            )
            return Response(reviews)
        elif request.method == "POST":
            user_id = request.user.id
            users_made_feedback = Feedback.objects.filter(product_id=pk).values_list(
                "user_id", flat=True
            )

            if user_id in users_made_feedback:
                return Response(
                    {"user": f"{request.user.username}", "answer": "Уже оставлял отзыв"}
                )
            data = request.data
            serializer = FeedbackSerializer(data=data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id:
            return Response(
                {"error": "Укажите product_id, это обязательное поле"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Такой товар не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(user=request.user.id).first()
        if not cart:
            return Response({"items": [], "total": 0})

        serializer = CartSerializer(cart)

        return Response(serializer.data)


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        new_quantity = request.data.get("quantity")
        try:
            cart_item = CartItem.objects.get(id=item_id)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Такого товара нет в корзине."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if new_quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart = cart_item.cart
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Товара нет в корзине"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CartSerializer(cart)
        return Response(serializer.data)


class ClearCartView(APIView):
    def delete(self, request):
        cart: Cart = Cart.objects.filter(user=request.user).first()

        if cart:
            cart.items.all().delete()
            return Response(
                {"message": "Корзина очищена"}, status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {"error": "Корзина не найдена"}, status=status.HTTP_404_NOT_FOUND
        )


class CreateOrderView(APIView):
    permission_classes = [IsOwnerOrReadOnly]  # [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):

        cart = get_cart_instance(request)

        product_out_of_stock = check_cart_products_out_of_stock(cart)
        if product_out_of_stock:
            return inform_user_that_products_out_of_stock(product_out_of_stock)

        with transaction.atomic():
            order = create_order(request, cart)

            cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(serializer.data)
