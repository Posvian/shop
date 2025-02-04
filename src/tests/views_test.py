from django.test import TestCase
from django.test import Client

import sys
import os

sys.path.insert(0, os.path.join(__file__, "../.."))


class TestShopsUrl(TestCase):
    def setUp(self) -> None:
        self.c = Client()

    def test_valid_shop_url(self):
        self.response = self.c.get("/mainapp/shops/")
        self.assertEqual(self.response.status_code, 200)
