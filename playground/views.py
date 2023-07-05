import logging

import requests
from django.core.mail import BadHeaderError
from django.db.models import Sum
from django.http.request import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage

from store.models import Product

from .tasks import send_emails_to_customers, sent_order_email

logger = logging.getLogger(__name__)


@cache_page(5 * 10)
def home(request: HttpRequest):
    products = Product.objects.values()
    send_emails_to_customers.delay("Hello customer")
    return render(request, "home.html", {"products": products})


class HomePage(APIView):
    @method_decorator(cache_page(2 * 60 * 60))
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


def send_store_email(request):
    sent_order_email.delay()
    return render(request, "home.html")


def say_hello(request):
    products = Product.objects.values().annotate(total_price=Sum("unit_price"))[:10]
    try:
        message = BaseEmailMessage(
            template_name="emails/email.html", context={"products": products}
        )
        message.send(["daudnamayala@gmail.com", "sailing@gmail.com", "admin@dj.com"])
    except BadHeaderError:
        ...
    return render(request, "home.html", context={"products": products})
