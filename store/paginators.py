from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """A paginator class for /products endpoint"""

    page_size = 20
    page_query_description = "Page"
