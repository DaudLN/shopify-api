from .common import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "lZmQiuSTxAWKOtPb4PxvFrwJNmIp259DJN2a9yqI7+9WWSdMZ56DONI4LFZlrt3H"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "silk",
    "django_extensions",
]

MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "silk.middleware.SilkyMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

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

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "workflow"

EMAIL_FROM = "noreply@example.com"

EMAIL_HOST_USER = ""

EMAIL_HOST_PASSWORD = ""

EMAIL_PORT = 2525

EMAIL_USE_TLS = False

EMAIL_USE_SSL = False

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
