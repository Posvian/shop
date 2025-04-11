from django.db import models
from mainapp.models import Cart, Product
from base.models import TimestampMixin


class CartItem(TimestampMixin):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_item"
