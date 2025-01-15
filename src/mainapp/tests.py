from django.test import TestCase
from django.test import Client


class TestView(TestCase):

    def test_view_product(self):
        client = Client()
        url = "/products/"
        response = client.get(url)
        self.assertEqual(response.status_code, 200)


# import unittest

#
# class SomeTest(unittest.TestCase):
#     def setUp(self):
#         super(SomeTest, self).setUp()
#         self.mock_data = [1, 2, 3, 4, 5]
#
#     def test(self):
#         self.assertEqual(len(self.mock_data), 5)
#
#     def tearDown(self):
#         super(SomeTest, self).tearDown()
#         self.mock_data = []
#
#
# if __name__ == "__main__":
#     unittest.main()
