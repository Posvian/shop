from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from authapp.models import CustomUser
from shop_api.views import (
    CustomUserViewSet,
    ProductViewSet,
    AddToCartView,
    CartDetailView,
    UpdateCartItemView,
    RemoveFromCartView,
    ClearCartView,
    CreateOrderView,
)

# from shop_api.views import UserAPIView
# from shop_api.views import custom_user_list, custom_user_detail

router = routers.SimpleRouter()
router.register(r"users", CustomUserViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    # path("v1/userlist/", UserAPIView.as_view()),
    # path("users/", custom_user_list),
    # path("users/<int:pk>/", custom_user_detail),
    # path("v1/users/", CustomUserViewSet.as_view({"get": "list"})),
    # path("v1/users/<int:pk>/", CustomUserViewSet.as_view({"put": "update"})),
    path("v1/", include(router.urls)),
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("v1/cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("v1/cart/", CartDetailView.as_view(), name="cart"),
    path(
        "v1/cart/update/<int:item_id>/",
        UpdateCartItemView.as_view(),
        name="update-cart-item",
    ),
    path(
        "v1/cart/remove/<int:item_id>/",
        RemoveFromCartView.as_view(),
        name="remove-from-cart",
    ),
    path("v1/cart/clear/", ClearCartView.as_view(), name="clear-cart"),
    path("v1/order/create/", CreateOrderView.as_view(), name="create-order"),
]
