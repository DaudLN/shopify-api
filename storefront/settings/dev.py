import os
import dj_database_url
from dotenv import load_dotenv

from .common import *

load_dotenv()
DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
    # "silk",
]

# MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")

# DATABASES = {
#     "default": dj_database_url.parse(DATABASE_URL),
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "storefront",
        "USER": "root",
        "PASSWORD": "MyPassword",
        "HOST": "mysql",
        "PORT": "3306",
    }
}


CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "db": "10",
            "TIMEOUT": 10 * 60,
            "parser_class": "redis.connection.PythonParser",
            "pool_class": "redis.BlockingConnectionPool",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


DEFAULT_FROM_EMAIL = "admin.store@storefront.com"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 2525

EMAIL_USE_TLS = False
