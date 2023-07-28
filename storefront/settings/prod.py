import os
import dj_database_url
from .common import *

DEBUG = False

ALLOWED_HOSTS = ["shopify-ed15.onrender.com"]

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
REDIS_URL = os.environ.get("REDIS_URL")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL),
}

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "db": "10",
            "TIMEOUT": 10 * 60,
            "parser_class": "redis.connection.PythonParser",
            "pool_class": "redis.BlockingConnectionPool",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
