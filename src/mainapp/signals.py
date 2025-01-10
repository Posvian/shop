from django.core.signals import request_finished
from django.core.validators import ValidationError
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from authapp.models import CustomUser
from .models import Product, Feedback, Order, DeliveryMethod, Tags


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
        send_mail(
            "Привет",
            f"Заказ {instance.id} оплачен.",
            "dmitryposvyansky@yandex.ru",
            [instance.user.email],
        )
        """
        TODO: почитать про SMTP и зарегистрировать приложение в гугл аккаунте
        
        """


@receiver(post_save, sender=Product)
def new_product_auto_tag(sender, instance, *args, **kwargs):
    tag = Tags.objects.get(name="Новинки")
    tag.product.add(instance)
    tag.save()
