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
    rating = models.DecimalField(
        default=0, max_digits=3, decimal_places=2, verbose_name="Rating"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "seller"
