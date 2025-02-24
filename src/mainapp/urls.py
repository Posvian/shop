from django.contrib import admin
from django.urls import path
from django.urls import include
from debug_toolbar.toolbar import debug_toolbar_urls

from .views import (
    products_view,
    shops_view,
    add_seller_view,
    FeedbackView,
    add_product_view,
)

urlpatterns = [
    path("products/", products_view),
    path("shops/", shops_view),
    path("add_shop/", add_seller_view),
    path("feedback/", FeedbackView.as_view(), name="paste_feedback"),
    path("add_product", add_product_view, name="add_product"),
]
