from django.db import models
from base.models import TimestampMixin


class Tags(TimestampMixin):
    product = models.ManyToManyField(to="Product")
    name = models.CharField(max_length=30, verbose_name="Tag")
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "Tags"
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
