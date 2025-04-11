from django.core.management.base import BaseCommand
from faker import Faker
from mainapp.models import Tags, Brand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        brands_list = []
        for i in range(600001, 700000):
            brands_list.append(Tags(name=f"brand_{i}"))

        Brand.objects.bulk_create(brands_list)

        self.stdout.write(self.style.SUCCESS("Great, it works!"))
