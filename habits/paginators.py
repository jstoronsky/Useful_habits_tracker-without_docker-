from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    page_size = 5
