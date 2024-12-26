from django.db import models
from base.models import TimestampMixin


class DeliveryInformation(TimestampMixin):
    address = models.CharField(max_length=400)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    delivery_method = models.ForeignKey(
        to="DeliveryMethod", on_delete=models.CASCADE, null=True
    )
