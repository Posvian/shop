from django.core.management.base import BaseCommand
from faker import Faker
from mainapp.models import Tags


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        tags_list = []
        for i in range(300001, 400000):
            tags_list.append(Tags(name=f"tag_{i}"))

        Tags.objects.bulk_create(tags_list)

        self.stdout.write(self.style.SUCCESS("Great, it works!"))
