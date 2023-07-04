from .common import *

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
    # "silk",
]

# MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]

SECRET_KEY = "django-insecure-1tcb$yxuvlbp@2*=hrq3&7*ah^%j$)@+7qdj0o1gc1+hj+jc&2"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "storefront",
        "USER": "admin",
        "PASSWORD": "@Davy2130",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}


CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
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
