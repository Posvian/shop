from django.db import models
from base.models import TimestampMixin


class Product(TimestampMixin):
    name = models.CharField(max_length=30, verbose_name='Name')
    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True
    )
    stock_balance = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='Price'
    )
    category = models.ForeignKey(
        to='Category',
        verbose_name='category',
        on_delete=models.CASCADE,
        null=True
    )
    brand = models.ForeignKey(
        to='Brand',
        verbose_name='brand',
        on_delete=models.CASCADE)
    rating = models.DecimalField(
        default=0,
        max_digits=3,
        decimal_places=2,
        verbose_name='Rating'
    )
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __delete__(self, *args):
        self.is_hidden = True
        self.save()

    class Meta:
        db_table = 'product'
