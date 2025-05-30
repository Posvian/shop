from threading import Event, Thread
from time import sleep

from django.db import connection
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework import status

import sys
import os

from authapp.models import CustomUser
from mainapp.models import Tags, Category, Brand, Seller, Product, Cart, CartItem, Order

sys.path.insert(0, os.path.join(__file__, "../.."))


class TestProductsView(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        Tags.objects.create(name="Новинки")
        Category.objects.create(name="Fruits", slug="fruits")
        Category.objects.create(name="Drinks", slug="drinks")
        Brand.objects.create(name="Pepsi")
        Brand.objects.create(name="Russia Fruits")
        Seller.objects.create(name="Lenta")
        CustomUser.objects.create_user(
            username="user_1", password="123", email="123@mail.ru"
        )
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

    def test_valid_products_url(self):
        response = self.c.get("/mainapp/products/")
        self.assertEqual(response.status_code, 200)

    def test_context_products(self):
        waiting_result = Product.objects.get(name="Banana")
        result = self.c.get("/mainapp/products/").context[0].dicts[3]["products"][0]
        self.assertEqual(waiting_result, result)


class TestShopsView(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        Seller.objects.create(name="Lenta")

    def test_view_url(self):
        url = "/mainapp/shops/"
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_shops(self):
        url = "/mainapp/shops/"
        waiting_result = Seller.objects.get(name="Lenta")
        result = self.c.get(url).context[0].dicts[3]["shops"][0]
        self.assertEqual(result, waiting_result)


# class TestFindHost(TransactionTestCase):
#     max_bill = 200
#
#     def setUp(self):
#         self.client = Client()
#         self.hobby = models.Hobby.objects.create(name="bookscrapping")
#         self.host = models.Host.objects.create(
#             name="Oleg", age=23, max_guest_bill=self.max_bill
#         )
#         self.host.hobbies.add(self.hobby)
#         self.pub = models.Pub.objects.create(
#             name="pub", lat=12, long=32, max_visitors=100, visitor_count=0
#         )
#         # self.first_guest = models.Guest.objects.create(
#         #     name='Hanna', age=25, desired_order_value=self.max_bill - 10
#         # )
#         # self.first_guest.hobbies.add(self.hobby)
#
#     def tearDown(self):
#         self.hobby.delete()
#         self.host.delete()
#         self.pub.delete()
#         # self.first_guest.delete()
#
#     def make_request(self, name):
#         url = reverse("friends:find_friend")
#         response = self.client.post(
#             url,
#             data={
#                 "name": name,
#                 "desired_order_value": self.max_bill - 10,
#                 "hobbies": [self.hobby.id],
#             },
#         )
#         self.assertEqual(response.status_code, 302)
#
#     def test_success(self):
#         original_make_arrangement = views.make_arrangement
#         event = threading.Event()
#
#         def new_behavior(*args, **kw):
#             event.wait(timeout=5)
#             return original_make_arrangement(*args, **kw)
#
#         with patch("friends.views.make_arrangement") as fake_make_arrangement:
#             fake_make_arrangement.side_effect = new_behavior
#             thread_hanna = threading.Thread(target=self.make_request, args=("Hanna",))
#             thread_irina = threading.Thread(target=self.make_request, args=("Irina",))
#             thread_hanna.start()
#             thread_irina.start()
#
#             sleep(1)
#             event.set()
#
#             thread_hanna.join(timeout=5)
#             thread_irina.join(timeout=5)
#
#         self.assertEqual(models.Arrangement.objects.count(), 1)


from django.test import TransactionTestCase, RequestFactory
from unittest.mock import patch
from shop_api.views import AddToCartView, CreateOrderView


class TestBuyProduct(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.rf = RequestFactory()
        Tags.objects.create(name="Новинки")
        Category.objects.create(name="Fruits", slug="fruits")
        Category.objects.create(name="Drinks", slug="drinks")
        Brand.objects.create(name="Pepsi")
        Brand.objects.create(name="Russia Fruits")
        Seller.objects.create(name="Lenta")
        CustomUser.objects.create_user(
            username="user_1", password="123", email="123@mail.ru"
        )
        CustomUser.objects.create_user(
            username="user_2", password="234", email="234@mail.ru"
        )
        Product.objects.create(
            name="Apple",
            stock_balance=1,
            category=Category.objects.get(name="Fruits"),
            brand=Brand.objects.get(name="Russia Fruits"),
            seller=Seller.objects.get(name="Lenta"),
            user=CustomUser.objects.get(username="user_2"),
        )
        Cart.objects.create(user=CustomUser.objects.get(username="user_1"))
        Cart.objects.create(user=CustomUser.objects.get(username="user_2"))
        CartItem.objects.create(
            cart=Cart.objects.get(user__username="user_1"),
            product=Product.objects.get(name="Apple"),
        )
        CartItem.objects.create(
            cart=Cart.objects.get(user__username="user_2"),
            product=Product.objects.get(name="Apple"),
        )

        self.results = {}

    def make_request(self, username, password, label):
        try:
            url = reverse("create-order")
            self.c.login(username=username, password=password)
            response = self.c.post(
                url,
                data={},
            )
            self.results[label] = response.status_code
        finally:
            connection.close()

    def test_succses(self):
        view_instance = CreateOrderView()
        original_make_order = view_instance.post

        event = Event()

        def new_behavior(request, *args, **kwargs):
            event.wait(timeout=5)
            return original_make_order(request, *args, **kwargs)

        with patch("shop_api.views.CreateOrderView.post") as fake_make_order:
            fake_make_order.side_effect = new_behavior
            thread_client_1 = Thread(
                target=self.make_request,
                args=("user_1", "123", "first"),
            )
            thread_client_2 = Thread(
                target=self.make_request,
                args=("user_2", "234", "second"),
            )
            # with self.assertRaises(IntegrityError):
            thread_client_1.start()
            thread_client_2.start()

            sleep(1)
            event.set()

        thread_client_1.join(timeout=5)
        thread_client_2.join(timeout=5)

        codes = set(self.results.values())
        self.assertIn(status.HTTP_200_OK, codes)
        self.assertIn(status.HTTP_400_BAD_REQUEST, codes)

        self.assertEqual(Order.objects.count(), 1)
