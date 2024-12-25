from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Product, Feedback


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")


@receiver(post_save, sender=Feedback)
def auto_update_product_rating(sender, instance, created, *args, **kwargs):
    print("signal work")
    ratings = Feedback.objects.filter(product=instance.product.id)
    print(ratings)
