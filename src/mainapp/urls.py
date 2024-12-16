from django.contrib import admin
from django.urls import path
from django.urls import include
from debug_toolbar.toolbar import debug_toolbar_urls

from .views import product_list

urlpatterns = [
    path("", product_list),
]
