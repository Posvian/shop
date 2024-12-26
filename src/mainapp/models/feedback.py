from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
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


# @receiver(post_save, sender=Feedback)
# def auto_update_product_rating(sender, instance, created, *args, **kwargs):
#     ratings = Feedback.objects.filter(product=instance.product.id)
#     ratings_sum = 0
#     for rating in ratings:
#         ratings_sum += rating.rating
#     new_product_rating = ratings_sum / len(ratings)
#     print(len(ratings))
#     product = Product.objects.get(id=instance.product.id)
#     product.rating = new_product_rating
#     product.save()
