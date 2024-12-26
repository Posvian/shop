from django.db import models
from base.models import TimestampMixin


class DeliveryMethod(TimestampMixin):
    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
