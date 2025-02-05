from django.test import TestCase
from django.test import Client

import sys
import os

from mainapp.models import Tags, Category, Brand, Seller, Product


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
        Product.objects.create(
            name="Apple",
            stock_balance=10,
            category=Category.objects.get(name="Fruits"),
            brand=Brand.objects.get(name="Russia Fruits"),
            seller=Seller.objects.get(name="Lenta"),
        )
        Product.objects.create(
            name="Banana",
            stock_balance=5,
            # category_id=1,
            category=Category.objects.get(name="Fruits"),
            brand=Brand.objects.get(name="Russia Fruits"),
            seller=Seller.objects.get(name="Lenta"),
        )

    def test_valid_products_url(self):
        response = self.c.get("/mainapp/products/")
        self.assertEqual(response.status_code, 200)

    def test_context_products(self):
        waiting_result = Product.objects.get(name="Apple")
        result = (
            self.c.get("/mainapp/products/").context[0].dicts[3]["products"][0]
        )
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
