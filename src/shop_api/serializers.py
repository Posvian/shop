from rest_framework import serializers

from authapp.models import CustomUser
from mainapp.models import Product, Feedback, CartItem, Cart, ProductInOrder


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "age", "email", "country")


class AddProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "stock_balance",
            "price",
            "category",
            "brand",
            "seller",
            "rating",
            "weight",
            "sales_count",
            "is_hidden",
            "user",
        )


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feedback
        fields = ("user", "product", "feedback", "rating")


class ProductCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("name", "price")


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("items", "total")

    def get_total(self, object: {items}):
        return sum(item.product.price * item.quantity for item in object.items.all())


class ProductInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrder
        fields = ("product", "quantity", "price")


class OrderSerializer(serializers.ModelSerializer):
    items = ProductInOrderSerializer(many=True)

    class Meta:
        model = 