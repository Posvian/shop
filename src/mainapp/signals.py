from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from authapp.models import CustomUser
from .models import Product, Feedback, Order, DeliveryMethod
from django.core.validators import ValidationError


@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")


@receiver(post_save, sender=Feedback)
def product_auto_update_rating(sender, instance, created, *args, **kwargs):
    ratings = Feedback.objects.filter(product=instance.product.id)
    ratings_sum = 0
    for rating in ratings:
        ratings_sum += rating.rating
    new_product_rating = ratings_sum / len(ratings)
    print(len(ratings))
    product = Product.objects.get(id=instance.product.id)
    product.rating = new_product_rating
    product.save()


@receiver(post_delete, sender=Product)
def feedback_auto_delete(sender, instance, *args, **kwargs):
    Feedback.objects.filter(product_id=instance.id).delete()


@receiver(post_save, sender=Order)
def product_sales_count_update(sender, instance, created, *args, **kwargs):
    if instance.is_delivered:
        product = Product.objects.get(id=instance.items.get().product_id)
        product.sales_count += 1
        product.save()


@receiver(pre_save, sender=DeliveryMethod)
def delivery_method_price_validator(sender, instance, *args, **kwargs):
    if instance.price < 1000:
        raise ValidationError(
            "Стоимость доставки должна быть больше 1000", code="invalid"
        )


@receiver(post_save, sender=Order)
def inform_order_user(sender, instance, created, *args, **kwargs):
    if instance.is_paid:
        print(
            f"{CustomUser.objects.get(id=instance.user_id)}, Ваш заказ оплачен"
        )
