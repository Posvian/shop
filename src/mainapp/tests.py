from django.test import TestCase

# from django.test import Client
#
#
# class TestView(TestCase):
#
#     def test_view_product(self):
#         client = Client()
#         url = "/products/"
#         response = client.get(url)
#         self.assertEqual(response.status_code, 200)


# import unittest

#
# class SomeTest(unittest.TestCase):
#     def setUp(self):
#         super(SomeTest, self).setUp()
#         self.mock_data = [1, 2, 3, 4, 5]
#
#     def test(self):
#         self.assertEqual(len(self.mock_data), 5)
#
#     def tearDown(self):
#         super(SomeTest, self).tearDown()
#         self.mock_data = []
#
#
# if __name__ == "__main__":
#     unittest.main()


# from unittest import TestCase
# from src.UniqueQueue import UniqueQueue
#
#
# class TestQueue(TestCase):
#     def setUp(self) -> None:
#         self.test_value_1 = 1
#         self.test_value_2 = 2
#         self.test_value_3 = 3
#         self.strategy = "FIFO"
#
#     def test_queue_exists(self):
#         queue = UniqueQueue()
#
#     def test_queue_exists_params(self):
#         strategy = "FIFO"
#         queue = UniqueQueue(strategy=strategy)
#
#     def test_validation_strategy_name(self):
#         strategy = "FOO"
#         with self.assertRaises(TypeError):
#             queue = UniqueQueue(strategy)
#
#     def test_add_item_in_queue(self):
#         queue = UniqueQueue(strategy=self.strategy)
#         queue.add_element(element=self.test_value_1)
#         value = queue.take_element()
#         self.assertEqual(self.test_value_1, value)
#
#     def test_add_multy_value(self):
#         queue = UniqueQueue(strategy=self.strategy)
#         queue.add_element(element=self.test_value_1)
#         queue.add_element(element=self.test_value_2)
#         queue.add_element(element=self.test_value_3)
#         value_1 = queue.take_element()
#         value_2 = queue.take_element()
#         value_3 = queue.take_element()
#         self.assertEqual(self.test_value_1, value_1)
#         self.assertEqual(self.test_value_2, value_2)
#         self.assertEqual(self.test_value_3, value_3)
#
#     def test_empty_queue(self):
#         queue = UniqueQueue(strategy=self.strategy)
#         value_1 = queue.take_element()
#         self.assertIsNone(value_1)


from django.test import TestCase
from src.UniqueQueue import UniqueQueue
from src.mainapp.models import ProductQueue, Product, Category, Brand, Seller


class TestUniqueQueue(TestCase):

    def setUp(self) -> None:
        Category.objects.create(name="Fruits", slug="fruits")
        Category.objects.create(name="Drinks", slug="drinks")
        Brand.objects.create(name="Pepsi")
        Brand.objects.create(name="Russia Fruits")
        Seller.objects.create(name="Lenta")
        Product.objects.create(
            name="Apple",
            stock_balance=10,
            category_id=1,
            brand_id=2,
            seller_id=1,
        )
        Product.objects.create(
            name="Banana",
            stock_balance=5,
            category_id=1,
            brand_id=2,
            seller_id=1,
        )
        Product.objects.create(
            name="Pepsi",
            stock_balance=15,
            category_id=2,
            brand_id=1,
            seller_id=1,
        )
        Product.objects.create(
            name="Coca-cola",
            stock_balance=10,
            category_id=2,
            brand_id=1,
            seller_id=1,
        )

    def test_object_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = f"{product.name}"
        self.assertEqual(expected_object_name, str(product))
