from django.db import models
from django.core.validators import FileExtensionValidator

from base.models import TimestampMixin
from base.services import validate_size_image


class Category(TimestampMixin):
    name = models.CharField(max_length=30, verbose_name='Name')
    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True)
    image = models.ImageField(
        upload_to='',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg']), validate_size_image]
        )
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
