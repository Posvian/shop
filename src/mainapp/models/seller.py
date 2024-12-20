from django.db import models
from base.models import TimestampMixin
from .product import Product


class Seller(TimestampMixin):
    name = models.CharField(max_length=40, verbose_name="seller")
    iin = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name="individual identification number",
    )
    country = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = "seller"
