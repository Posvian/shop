from django.contrib import admin
from mainapp.models.product import Product
from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.delivery_information import DeliveryInformation
from mainapp.models.delivery_method import DeliveryMethod
from mainapp.models.feedback import Feedback
from mainapp.models.order import Order
from mainapp.models.product_in_order import ProductInOrder
from mainapp.models.seller import Seller
from mainapp.models.tag import Tags
from authapp.models.custom_user import CustomUser


@admin.action(description="Mark selected orders as shipped")
def make_shipped(modeladmin, request, queryset):
    queryset.update(is_shipped=True)


@admin.action(description="Delete bad feedbacks")
def delete_bad_feedbacks(modeladmin, request, queryset):
    queryset.filter(rating__lt=3).delete()


class ProductInline(admin.StackedInline):
    model = Product


class DeliveryInformationInline(admin.StackedInline):
    model = DeliveryInformation


class OrderInline(admin.StackedInline):
    model = Order


class TagsInline(admin.TabularInline):
    model = Tags.product.through


class ProuctInOrderInline(admin.StackedInline):
    model = ProductInOrder


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "stock_balance", "price"]
    list_filter = ["category", "seller"]
    search_fields = ["name", "description"]
    inlines = [TagsInline, ProuctInOrderInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(DeliveryInformation)
class DeliveryInformationAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    inlines = [DeliveryInformationInline]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "feedback", "rating"]
    search_fields = ["feedback", "user__first_name"]
    actions = [delete_bad_feedbacks]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "delivery_info",
        "final_price",
        "is_paid",
        "is_shipped",
        "is_delivered",
    ]
    list_filter = ["is_paid", "is_shipped"]
    inlines = [ProuctInOrderInline]
    actions = [make_shipped]


@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "iin", "country", "rating")
    search_fields = ["name"]
    list_filter = ("country", "rating")


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    inlines = [TagsInline]
    exclude = ["product"]


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
