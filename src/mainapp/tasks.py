import base64

import requests
from django.core.files.base import ContentFile
from celery import shared_task

from .models import Product


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
        category_id=category,
        brand_id=brand,
        seller_id=seller,
        weight=weight,
        image=image,
    )


@shared_task
def add(x, y):
    return x + y
