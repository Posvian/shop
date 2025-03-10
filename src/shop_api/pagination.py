from rest_framework.pagination import PageNumberPagination


class FiveResultsSetPagination(PageNumberPagination):
    page_size = 5
