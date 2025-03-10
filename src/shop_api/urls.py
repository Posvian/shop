from django.urls import path, include
from rest_framework import routers
from authapp.models import CustomUser
from shop_api.views import CustomUserViewSet, ProductViewSet

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
]
