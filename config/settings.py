from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local Apps
    'apps.accounts.apps.AccountsConfig',
    'apps.hotels.apps.HotelsConfig',
    "apps.bookings.apps.BookingsConfig",
    "rest_framework",
    "drf_spectacular",
    "apps.api",
    'rest_framework_simplejwt.token_blacklist',
]

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------------------------------------------------------
# URL Configuration
# -----------------------------------------------------------------------------

ROOT_URLCONF = 'config.urls'

# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -----------------------------------------------------------------------------
# WSGI
# -----------------------------------------------------------------------------

WSGI_APPLICATION = 'config.wsgi.application'

# -----------------------------------------------------------------------------
# Database (SQLite for now)
# Later replace with PostgreSQL
# -----------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DATABASE_ENGINE",
            "django.db.backends.sqlite3"
        ),
        "NAME": BASE_DIR / os.getenv(
            "DATABASE_NAME",
            "db.sqlite3"
        ),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# -----------------------------------------------------------------------------
# Password Validation
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True

# -----------------------------------------------------------------------------
# Static Files
# -----------------------------------------------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# -----------------------------------------------------------------------------
# Media Files
# -----------------------------------------------------------------------------

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------------------------------------------------------
# Authentication
# -----------------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.CustomUser"

LOGIN_URL = "login"

# LOGIN_REDIRECT_URL = "dashboard"

LOGOUT_REDIRECT_URL = "login"

# -----------------------------------------------------------------------------
# Default Primary Key
# -----------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------------
# REST API Integration
# -----------------------------------------------------------------------------

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}

# REST_FRAMEWORK = {
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
# }

# -----------------------------------------------------------------------------
# Swagger / OpenAPI Configuration
# -----------------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
    "TITLE": "HamroEase API",
    "DESCRIPTION": "Hotel Booking Management REST API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,

    "TAGS": [
        {
            "name": "Authentication",
            "description": "User authentication and account management.",
        },
        {
            "name": "Hotels",
            "description": "Hotel management endpoints.",
        },
        {
            "name": "Rooms",
            "description": "Room management endpoints.",
        },
        {
            "name": "Bookings",
            "description": "Booking management endpoints.",
        },
        {
            "name": "Payments",
            "description": "Payment related endpoints.",
        },
        {
            "name": "Reviews",
            "description": "Review management endpoints.",
        },
    ],
}

# -----------------------------------------------------------------------------
# Email Integration
# -----------------------------------------------------------------------------


EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = os.getenv("EMAIL_HOST")

EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "HamroEase <noreply@hamroease.com>"
)

# Stripe

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


# Khalti

KHALTI_SECRET_KEY = os.getenv("KHALTI_SECRET_KEY")
KHALTI_PUBLIC_KEY = os.getenv("KHALTI_PUBLIC_KEY")