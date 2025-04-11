from django.core.management.base import BaseCommand
from faker import Faker
from mainapp.models import Seller

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        shop_list = []
        for i in range(100001, 200000):
            shop_list.append(
                Seller(
                    name=f"shop_{i}",
                    iin=fake.unique.bothify(text="##########"),
                    country=fake.country(),
                )
            )
        Seller.objects.bulk_create(shop_list)

        self.stdout.write(self.style.SUCCESS("Great, it works!"))
