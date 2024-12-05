from django.db import models
from base.models import TimestampMixin


class ProductInOrder(TimestampMixin):
    order = models.ForeignKey(
        to='Order',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        to='Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'product_in_order'
