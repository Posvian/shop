from unittest.mock import MagicMock

from django.test import TestCase
from django.test import Client

from authapp.models import CustomUser
from mainapp.models import Seller, Tags, Category, Brand, Product, Feedback


class TestSellerForm(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_seller_form(self):
        name = "Dima"
        iin = 123456789
        country = "Russia"
        self.response = self.client.post(
            "/mainapp/add_shop/",
            {"name": name, "iin": iin, "country": country},
        )
        self.assertEqual(self.response.status_code, 302)
        seller = Seller.objects.all()
        self.assertEqual(len(seller), 1)
        self.assertEqual(seller[0].name, name)
        self.assertEqual(seller[0].iin, str(iin))
        self.assertEqual(seller[0].country, country)


class TestFeedbackForm(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        CustomUser.objects.create(
            username="Posvian",
            first_name="Dima",
            last_name="Posvianskii",
            email="email@email.ru",
        )
        Tags.objects.create(name="Новинки")
        Category.objects.create(name="Fruits", slug="fruits")
        Brand.objects.create(name="Russia Fruits")
        Seller.objects.create(name="Lenta")
        Product.objects.create(
            name="Apple",
            stock_balance=10,
            category=Category.objects.get(name="Fruits"),
            brand=Brand.objects.get(name="Russia Fruits"),
            seller=Seller.objects.get(name="Lenta"),
            user=CustomUser.objects.get(username="Posvian"),
        )

    def test_add_feedback(self):
        user = CustomUser.objects.first()
        product = Product.objects.first()
        feedback = "Good"
        rating = 5
        self.response = self.client.post(
            "/mainapp/feedback/",
            {
                "user": user.id,
                "product": product.id,
                "feedback": feedback,
                "rating": rating,
            },
        )
        self.assertEqual(self.response.status_code, 302)
        added_feedback = Feedback.objects.all()
        self.assertEqual(len(added_feedback), 1)
        self.assertEqual(added_feedback[0].user, user)
        self.assertEqual(added_feedback[0].product, product)
        self.assertEqual(added_feedback[0].feedback, feedback)
        self.assertEqual(added_feedback[0].rating, rating)
