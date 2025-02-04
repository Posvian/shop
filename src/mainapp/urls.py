from django.contrib import admin
from django.urls import path
from django.urls import include
from debug_toolbar.toolbar import debug_toolbar_urls

from .views import products_view, shops_view

urlpatterns = [
    path("products/", products_view),
    path("shops/", shops_view),
]
