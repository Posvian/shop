from .order import Order
from .brand import Brand
from .category import Category
from .product import Product
from .product_in_order import ProductInOrder
from .delivery_information import DeliveryInformation
from .feedback import Feedback
from .seller import Seller

from django.db.models.signals import post_save


# # @receiver(post_save, sender=Product)
# def product_created(sender, instance, **kwargs):
#     print("signal work")
#     print(sender)
#     print(instance)
#     product = Product.objects.get(id=instance.id)
#     if product.seller.country == "Italy":
#         print("Great!")
#
#
# post_save.connect(receiver=product_created, sender=Product)
