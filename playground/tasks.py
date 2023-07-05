import time
from celery import shared_task

from store.models import Product
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_emails_to_customers(message):
    print("Sending 10k emails to customers")
    print(message)
    time.sleep(10)
    print("Done sending emails")


@shared_task
def sent_order_email():
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
