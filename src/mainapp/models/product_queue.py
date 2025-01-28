from django.db import models


class ProductQueue(models.Model):
    product = models.ForeignKey(to="Product", on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "product_queue"
