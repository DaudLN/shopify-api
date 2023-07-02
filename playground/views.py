import logging

import requests
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView

from store.models import Product

from .tasks import send_emails_to_customers

# Create your views here.

# Low level cache API
# def home(request: HttpRequest):
#     key = "products"
#     if cache.get(key) is None:
#         products = Product.objects.values()
#         cache.set(key, products)
#     send_emails_to_customers.delay("Hello customer")
#     return render(request, "home.html", {"products": cache.get(key)})


logger = logging.getLogger(__name__)


@cache_page(5 * 10)
def home(request: HttpRequest):
    products = Product.objects.values()
    send_emails_to_customers.delay("Hello customer")
    return render(request, "home.html", {"products": products})


class HomePage(APIView):
    # @method_decorator(cache_page(5 * 10))
    def get(self, request):
        try:
            logger.info("Sending request to the backend")
            products = Product.objects.values()
            logger.info("Sending emails to customers")
            send_emails_to_customers.delay("Hello customer")
            logger.info("Sending emails to customers done")
            logger.info("Sending request to the backend success")
        except requests.ConnectionError:
            logger.critical("Server is offline")
        return render(request, "home.html", {"products": products})
