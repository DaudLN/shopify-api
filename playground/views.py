import logging


from rest_framework.views import APIView
from rest_framework.response import Response

from store.models import Product


class HomePage(APIView):
    # @method_decorator(cache_page(2 * 60 * 60))
    def get(self, request):
        return Response({"message": "Hello world"})
