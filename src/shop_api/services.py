from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status

from config import settings
from mainapp.models import Cart, Order, ProductInOrder, Product
from authapp.models import CustomUser


def delete_cache(key_prefix: str):
    keys_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)


def get_cart_instance(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.items.count() == 0:
        return Response(
            {"error": "Корзина пуста или не существует"},
            status=status.HTTP_404_NOT_FOUND,
        )
    return cart


def check_cart_products_out_of_stock(cart: Cart):
    product_out_of_stock = []
    for item in cart.items.all():
        if item.product.stock_balance < item.quantity:
            product_out_of_stock.append(
                {
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "доступно": item.product.stock_balance,
                }
            )
    return product_out_of_stock


def inform_user_that_products_out_of_stock(product_list):
    return Response(
        {
            "error": "В корзине есть недоступные товары",
            "Недоступные товары": product_list,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


def count_final_price(cart: Cart):
    return sum(item.product.price * item.quantity for item in cart.items.all())


def product_in_order_create(order: Order, cart: Cart):
    for item in cart.items.all():
        # try:
        #     item.product.stock_balance = F("stock_balance") - item.quantity
        #     item.product.save()
        # except IntegrityError:
        #     return Response(
        #         {
        #             "error": "В корзине есть недоступные товары",
        #             "Недоступные товары": item.product,
        #         },
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=item.product.id)

            if product.stock_balance <= 0:
                raise IntegrityError("Нет товара")

            product.stock_balance = F("stock_balance") - item.quantity
            product.save()

            ProductInOrder.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )


def create_order(request, cart: Cart):
    order = Order.objects.create(
        user=request.user,
        final_price=count_final_price(cart),
    )
    product_in_order_create(order, cart)

    return order
