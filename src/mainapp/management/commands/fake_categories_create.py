from django.core.management.base import BaseCommand
from faker import Faker
from mainapp.models import Category


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories_list = []
        for i in range(400001, 500000):
            categories_list.append(
                Category(
                    name=f"category_{i}",
                    description=fake.sentence(nb_words=10),
                    slug=f"category_{i}",
                )
            )

        Category.objects.bulk_create(categories_list)

        self.stdout.write(self.style.SUCCESS("Great, it works!"))
