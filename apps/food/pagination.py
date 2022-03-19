from rest_framework.pagination import PageNumberPagination


class FoodPagination(PageNumberPagination):
    page_size = 3
