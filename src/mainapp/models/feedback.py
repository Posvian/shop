from django.db import models
from base.models import TimestampMixin
from authapp.models import CustomUser
from .product import Product


RATING = (
    (5, "⭐⭐⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (3, "⭐⭐⭐"),
    (2, "⭐⭐"),
    (1, "⭐"),
)


class Feedback(TimestampMixin):
    user = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, related_name="feedback"
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="feedback"
    )
    feedback = models.TextField(default="No feedback", verbose_name="feedback")
    rating = models.SmallIntegerField(
        choices=RATING, default=5, verbose_name="rating"
    )

    def __str__(self):
        return f"{self.product} {self.user}"
