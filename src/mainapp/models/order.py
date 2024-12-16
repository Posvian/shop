from django.db import models
from base.models import TimestampMixin
from authapp.models import CustomUser
from .delivery_information import DeliveryInformation


class Order(TimestampMixin):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
    )
    delivery_info = models.ForeignKey(
        to=DeliveryInformation, on_delete=models.CASCADE, null=True
    )
    final_price = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        db_table = "order"

    def __str__(self):
        return f"Номер заказа {self.id}, сумма заказа {self.final_price}"
