from django.contrib import admin
from django.db.models import Count, F
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


class CountProductInOrderListFilter(admin.SimpleListFilter):
    title = "Количество товаров"
    parameter_name = "items"

    def lookups(self, request, model_admin):
        return [
            ("1", "1 товар"),
            ("2_5", "2-5 товаров"),
            ("6_", "6 и более товаров"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.annotate(Count("items")).filter(items__count=1)

        if self.value() == "2_5":
            return queryset.annotate(Count("items")).filter(
                items__count__gte=2, items__count__lte=5
            )

        if self.value() == "6_":
            return queryset.annotate(Count("items")).filter(items__count__gt=5)
        return queryset


@admin.action(description="Mark selected orders as shipped")
def make_shipped(modeladmin, request, queryset):
    queryset.update(is_shipped=True)


@admin.action(description="Delete bad feedbacks")
def delete_bad_feedbacks(modeladmin, request, queryset):
    queryset.filter(rating__lt=3).delete()


@admin.action(description="Make 10 percent discount")
def make_discount_product(modeladmin, request, queryset):
    for obj in queryset:
        price = obj.price
        new_price = price - price / 100 * 10
        obj.price = new_price
        obj.save()


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
    list_display = ["name", "description", "stock_balance", "price", "rating"]
    list_filter = ["category", "seller"]
    search_fields = ["name", "description"]
    inlines = [TagsInline, ProuctInOrderInline]
    actions = [make_discount_product]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "number_of_products"]
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
    list_filter = ["is_paid", "is_shipped", CountProductInOrderListFilter]
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
