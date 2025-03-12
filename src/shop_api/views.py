from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from authapp.models import CustomUser
from mainapp.models import Product, Feedback
from shop_api.filters import ProductFilter
from shop_api.pagination import FiveResultsSetPagination
from shop_api.permissions import IsOwnerOrReadOnly
from shop_api.serializers import (
    CustomUserSerializer,
    ProductSerializer,
    FeedbackSerializer,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    pagination_class = FiveResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = ProductFilter
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    @action(methods=["get", "post"], detail=True)
    def review(self, request, pk=None):
        if request.method == "GET":
            reviews = Feedback.objects.filter(product_id=pk).values(
                "user", "feedback", "rating"
            )
            return Response(reviews)
        elif request.method == "POST":
            user_id = request.user.id
            users_made_feedback = Feedback.objects.filter(product_id=1).values_list(
                "user_id", flat=True
            )

            if user_id in users_made_feedback:
                return Response(
                    {"user": f"{request.user.name}", "answer": "Уже оставлял отзыв"}
                )
            data = request.data
            serializer = FeedbackSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )


# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from authapp.models import CustomUser
# from shop_api.serializers import CustomUserSerializer
#
#
# @csrf_exempt
# def custom_user_list(request):
#     if request.method == "GET":
#         users = CustomUser.objects.all()
#         serializer = CustomUserSerializer(users, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = CustomUserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def custom_user_detail(request, pk):
#     try:
#         user = CustomUser.objects.get(id=pk)
#     except CustomUser.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == "GET":
#         serializer = CustomUserSerializer(user)
#         return JsonResponse(serializer.data)
#
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = CustomUserSerializer(user, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#         user.delete()
#         return HttpResponse(status=204)
