# from django.test import TestCase
# from src.UniqueQueue import UniqueQueue
# from src.mainapp.models import ProductQueue, Product, Category, Brand, Seller
#
#
# class TestUniqueQueue(TestCase):
#
#     def setUp(self) -> None:
#         Category.objects.create(name="Fruits", slug="fruits")
#         Category.objects.create(name="Drinks", slug="drinks")
#         Brand.objects.create(name="Pepsi")
#         Brand.objects.create(name="Russia Fruits")
#         Seller.objects.create(name="Lenta")
#         Product.objects.create(
#             name="Apple",
#             stock_balance=10,
#             category_id=1,
#             brand_id=2,
#             seller_id=1,
#         )
#         Product.objects.create(
#             name="Banana",
#             stock_balance=5,
#             category_id=1,
#             brand_id=2,
#             seller_id=1,
#         )
#         Product.objects.create(
#             name="Pepsi",
#             stock_balance=15,
#             category_id=2,
#             brand_id=1,
#             seller_id=1,
#         )
#         Product.objects.create(
#             name="Coca-cola",
#             stock_balance=10,
#             category_id=2,
#             brand_id=1,
#             seller_id=1,
#         )
#
#     def test_object_name(self):
#         product = Product.objects.get(id=1)
#         expected_object_name = f"{product.name}"
#         self.assertEqual(expected_object_name, str(product))
