from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    """
    Пагинация для привычек
    Attributes:
        page_size (int): Количество элементов на одной странице
        page_size_query_param (str): Позволяет клиенту запрашивать разное количество элементов
        max_page_size (int): Максимальное количество элементов на одной странице
    """

    page_size = 5  # Количество элементов на одной странице
    page_size_query_param = "page_size"  # Позволяет клиенту запрашивать разное количество элементов
    max_page_size = 10  # Максимальное количество элементов на одной странице
