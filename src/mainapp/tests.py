# from django.test import TestCase

from django.test import Client
from django.test import TestCase
from UniqueQueue import UniqueQueue
from authapp.models import CustomUser
from mainapp.models.product_queue import ProductQueue
from mainapp.models.product import Product
from mainapp.models.seller import Seller
from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.tag import Tags


class TestUniqueQueue(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.LIFO_strategy = "LIFO"
        self.FIFO_strategy = "FIFO"
        Tags.objects.create(name="Новинки")
        Category.objects.create(name="Fruits", slug="fruits")
        Category.objects.create(name="Drinks", slug="drinks")
        Brand.objects.create(name="Pepsi")
        Brand.objects.create(name="Russia Fruits")
        Seller.objects.create(name="Lenta")
        CustomUser.objects.create_user(
            username="user_2", password="234", email="234@mail.ru"
        )
        Product.objects.create(
            name="Apple",
            stock_balance=10,
            category=Category.objects.get(name="Fruits"),
            brand=Brand.objects.get(name="Russia Fruits"),
            seller=Seller.objects.get(name="Lenta"),
            user=CustomUser.objects.get(username="user_2"),
        )
        Product.objects.create(
            name="Banana",
            stock_balance=5,
            # category_id=1,
            category=Category.objects.get(name="Fruits"),
            brand=Brand.objects.get(name="Russia Fruits"),
            seller=Seller.objects.get(name="Lenta"),
            user=CustomUser.objects.get(username="user_2"),
        )
        Product.objects.create(
            name="Pepsi",
            stock_balance=15,
            category=Category.objects.get(name="Drinks"),
            brand=Brand.objects.get(name="Pepsi"),
            seller=Seller.objects.get(name="Lenta"),
            user=CustomUser.objects.get(username="user_2"),
        )
        Product.objects.create(
            name="Coca-cola",
            stock_balance=0,
            category=Category.objects.get(name="Drinks"),
            brand=Brand.objects.get(name="Pepsi"),
            seller=Seller.objects.get(name="Lenta"),
            user=CustomUser.objects.get(username="user_2"),
        )

    def test_queue_exists(self):
        queue = UniqueQueue()

    def test_validation_strategy(self):
        strategy = "FOO"
        with self.assertRaises(TypeError):
            queue = UniqueQueue(strategy=strategy)

    def test_product_create(self):
        Product.objects.get(name="Apple")

    def test_add_element_LIFO_strategy(self):
        queue = UniqueQueue(strategy=self.LIFO_strategy)
        queue.add_element(Product.objects.get(name="Apple"))
        self.assertEqual(
            ProductQueue.objects.first().product_id,
            Product.objects.get(name="Apple").id,
        )

    def test_add_element_FIFO_strategy(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        queue.add_element(Product.objects.get(name="Apple"))
        self.assertEqual(
            ProductQueue.objects.first().product_id,
            Product.objects.get(name="Apple").id,
        )

    def test_add_product_twice(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        first_product = Product.objects.get(name="Apple")
        second_product = Product.objects.get(name="Apple")
        first_product = queue.add_element(first_product)
        second_product = queue.add_element(second_product)
        self.assertEqual(first_product, second_product)

    def test_take_element_from_empty_queue(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        with self.assertRaises(NotImplementedError):
            queue.take_element()

    def test_LIFO_take_element(self):
        queue = UniqueQueue(strategy=self.LIFO_strategy)
        queue.add_element(Product.objects.get(name="Apple"))
        queue.add_element(Product.objects.get(name="Banana"))
        product = Product.objects.get(name="Banana")
        result = queue.take_element()
        self.assertEqual(product, result)

    def test_FIFO_take_element(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        queue.add_element(Product.objects.get(name="Apple"))
        queue.add_element(Product.objects.get(name="Banana"))
        product = Product.objects.get(name="Apple")
        result = queue.take_element()
        self.assertEqual(product, result)

    # def test_add_some_elements(self):
    #     queue = UniqueQueue(strategy=self.FIFO_strategy)
    #     product_1 = Product.objects.get(name="Apple")
    #     product_2 = Product.objects.get(name="Banana")
    #     product_3 = Product.objects.get(name="Pepsi")
    #     queue.add_element(product_1, product_2, product_3)
    #     value_1 = queue.take_element()
    #     value_2 = queue.take_element()
    #     value_3 = queue.take_element()
    #     self.assertEqual(product_1, value_1)
    #     self.assertEqual(product_2, value_2)
    #     self.assertEqual(product_3, value_3)

    def test_empty_DB(self):
        waiting_result = 0
        result = len(ProductQueue.objects.all())
        self.assertEqual(waiting_result, result)

    def test_priority_correct(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        product = Product.objects.get(name="Apple")
        priority = 2
        queue.add_element(product, priority=priority)
        priority_from_queue = ProductQueue.objects.first().priority
        self.assertEqual(priority, priority_from_queue)

    def test_priority_validation(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        product = Product.objects.get(name="Apple")
        priority = 5
        with self.assertRaises(ValueError):
            queue.add_element(product, priority=priority)

    # def test_incorrect_data(self):
    #     queue = UniqueQueue(strategy=self.FIFO_strategy)
    #     product = Product.objects.get(name="Apple")
    #     priority = 2
    #     with self.assertRaises(ValueError):
    #         queue.add_element(product, "adsaf", priority=priority)

    def test_product_out_of_stock(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        product = Product.objects.get(name="Coca-cola")
        queue.add_element(product)
        with self.assertRaises(NotImplementedError):
            queue.take_element()

    def test_make_stock_balance_into_sales_count(self):
        queue = UniqueQueue(strategy=self.FIFO_strategy)
        product = Product.objects.get(name="Apple")
        sales_count = product.sales_count
        stock_balance = product.stock_balance
        waiting_sales_count = sales_count + 1
        waiting_stock_balance = stock_balance - 1
        queue.add_element(product)
        updated_product = Product.objects.get(name="Apple")
        self.assertEqual(waiting_stock_balance, updated_product.stock_balance)
        self.assertEqual(waiting_sales_count, updated_product.sales_count)
