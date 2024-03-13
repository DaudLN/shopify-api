import os
import dj_database_url
from .common import *

DEBUG = False

ALLOWED_HOSTS = [host for host in os.environ.get("ALLOWED_HOSTS").split(",") if host]
SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
}

CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "db": "10",
            "TIMEOUT": 10 * 60,
            "parser_class": "redis.connection.PythonParser",
            "pool_class": "redis.BlockingConnectionPool",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ.get("EMAIL_HOST")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

EMAIL_PORT = int(os.getenv("EMAIL_PORT"))

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")=="True"

EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")=="True"