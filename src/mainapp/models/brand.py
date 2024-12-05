from django.db import models
from base.models import TimestampMixin


class Brand(TimestampMixin):
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        error_messages={
            'unique': 'Такой бренд уже существует.'
        }
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'
