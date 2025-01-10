from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_delete
from base.models import TimestampMixin


class Product(TimestampMixin):
    name = models.CharField(max_length=30, verbose_name="Name")
    description = models.TextField(
        verbose_name="Description", blank=True, null=True
    )
    stock_balance = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name="Price"
    )
    category = models.ForeignKey(
        to="Category",
        verbose_name="category",
        on_delete=models.CASCADE,
        null=True,
    )
    brand = models.ForeignKey(
        to="Brand", verbose_name="brand", on_delete=models.CASCADE
    )
    seller = models.ForeignKey(
        to="Seller", on_delete=models.CASCADE, verbose_name="seller", default=1
    )
    rating = models.DecimalField(
        default=0, max_digits=3, decimal_places=2, verbose_name="Rating"
    )
    weight = models.DecimalField(max_digits=5, decimal_places=3, default=1)
    sales_count = models.PositiveIntegerField(default=0)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __delete__(self, *args):
        self.is_hidden = True
        self.save()

    class Meta:
        db_table = "product"


# @receiver(post_delete, sender=Product)
# def feedback_auto_delete(sender, instance, *args, **kwargs):
#     Feedback.objects.filter(product_id=instance.id).delete()
