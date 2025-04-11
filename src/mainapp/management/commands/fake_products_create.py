from django.core.management.base import BaseCommand
from faker import Faker
from mainapp.models import Category, Brand, Seller, Product
from authapp.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = Category.objects.all()[50000:90000]
        brands = Brand.objects.all()[50000:90000]
        sellers = Seller.objects.all()[50000:90000]

        users = CustomUser.objects.all()
        start = 6451000
        stop = 6491000
        for k in range(100):
            products_list = []
            for i in range(start, stop):
                products_list.append(
                    Product(
                        name=f"product_{i}",
                        description=fake.sentence(nb_words=10),
                        stock_balance=fake.random_int(min=5, max=100),
                        price=fake.random_int(min=300, max=100000),
                        category=fake.random_element(categories),
                        brand=fake.random_element(brands),
                        seller=fake.random_element(sellers),
                        user=fake.random_element(users),
                    )
                )

            Product.objects.bulk_create(products_list)

            self.stdout.write(self.style.SUCCESS("Great, it works!"))
            start += 50000
            stop += 50001
