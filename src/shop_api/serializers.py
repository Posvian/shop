from rest_framework import serializers

from authapp.models import CustomUser
from mainapp.models import Product, Feedback


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "age", "email", "country")


class ProductSerializer(serializers.ModelSerializer):
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
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feedback
        fields = "__all__"
