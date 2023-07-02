import time
from celery import shared_task


@shared_task
def send_emails_to_customers(message):
    print("Sending 10k emails to customers")
    print(message)
    time.sleep(10)
    print("Done sending emails")
