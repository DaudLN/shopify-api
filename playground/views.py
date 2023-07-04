import logging

import requests
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.db.models import Sum
from django.http.request import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage

from store.models import Product

from .tasks import send_emails_to_customers

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
    products = Product.objects.values().annotate(total_price=Sum("unit_price"))[:10]
    # Render the HTML content from the template
    html_content = render_to_string("emails/email.html", context={"products": products})

    # Create a plain text version of the email (optional)
    text_content = strip_tags(html_content)

    try:
        # Create the email message
        email = EmailMultiAlternatives(
            "Thanks for your order",
            text_content,
            to=["daudnamayala@gmail.com", "sailing@gmail.com", "admin@dj.com"],
        )
        email.attach_file("media/images/products/me.jpg")
        # Attach the HTML content
        email.attach_alternative(html_content, "text/html")

        # Send the email
        email.send()
    except BadHeaderError:
        pass
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
