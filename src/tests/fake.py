from faker import Faker
from django.test import TestCase
from UniqueQueue import UniqueQueue
from mainapp.models.product_queue import ProductQueue
from mainapp.models.product import Product
from mainapp.models.seller import Seller
from mainapp.models.brand import Brand
from mainapp.models.category import Category
from mainapp.models.tag import Tags

fake = Faker()


class TestUniqueQueue(TestCase):

    def setUp(self) -> None:
        Tags.objects.create(name="Новинки")
        for i in range(10000):
            Category.objects.create(name=fake.name(), slug=f"slug_{i}")
        for i in range(10000):
            Brand.objects.create(name=f"brand_{i}")
        for _ in range(10000):
            Seller.objects.create(name=fake.name())
        categories = Category.objects.all()
        brands = Brand.objects.all()
        sellers = Seller.objects.all()
        for _ in range(10000):
            Product.objects.create(
                name=fake.name(),
                stock_balance=fake.random_int(min=5, max=100),
                category=fake.random_element(categories),
                brand=fake.random_element(brands),
                seller=fake.random_element(sellers),
            )

    def test_product_objects_create(self):
        count_products = len(Product.objects.all())
        self.assertEqual(count_products, 10000)
