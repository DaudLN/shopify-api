from django.urls import path
from .views import HomePage, send_store_email, say_hello


urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("mail/", send_store_email, name="email"),
    path("hello/", say_hello, name="say_hello"),
]
