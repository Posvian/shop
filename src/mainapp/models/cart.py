from django.db import models
from authapp.models import CustomUser
from base.models import TimestampMixin


class Cart(TimestampMixin):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        db_table = "cart"
