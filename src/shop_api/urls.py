from django.urls import path

# from shop_api.views import UserAPIView
from shop_api.views import custom_user_list, custom_user_detail

urlpatterns = [
    # path("v1/userlist/", UserAPIView.as_view()),
    path("users/", custom_user_list),
    path("users/<int:pk>/", custom_user_detail),
]
