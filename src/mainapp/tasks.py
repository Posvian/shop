import base64

import requests
from django.core.files.base import ContentFile
from celery import shared_task
from celery.schedules import crontab

from config.celery import app
from .models import Product, Category, Brand, Seller


@shared_task
def make_image(
    name, description, stock_balance, price, category, brand, seller, weight
):
    response = requests.post(
        "https://bf.dallemini.ai/generate", json={"prompt": description}
    )
    data = base64.b64decode(response.json()["images"][0])
    image = ContentFile(data, name="hello.png")
    Product.objects.create(
        name=name,
        description=description,
        stock_balance=stock_balance,
        price=price,
        category=Category.objects.get(id=int(category)),
        brand=Brand.objects.get(id=int(brand)),
        seller=Seller.objects.get(id=int(seller)),
        weight=weight,
        image=image,
    )


@shared_task
def add(x, y):
    return x + y


@app.task
def test(arg):
    print(arg)


app.conf.beat_schedule = {
    "print-every-220-seconds": {
        "task": "tasks.test",
        "schedule": 220.0,
        "args": "Hello!",
    }
}
