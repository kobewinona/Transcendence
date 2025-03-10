import os
from pathlib import Path
from datetime import timedelta
from project.constants import REFRESH_TOKEN_LIFETIME_DAYS, ACCESS_TOKEN_LIFETIME_MINUTES

# noinspection PyUnresolvedReferences
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv()

STATIC_URL = "/static/"
STATIC_ROOT = "/usr/src/app/staticfiles"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-k1!svx5pna71t3&y#w!9iie&5p2)7)0acb9%@k788a@2y=9r54"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Ensure secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173",  # dev
]
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrf-token",
    "x-requested-with",
]

CSP_CONNECT_SRC = (
    "'self'",
    "http://localhost:8001",
    "wss://localhost",
)

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "https://localhost",
]

REST_FRAMEWORK = {
    "STATIC_URL": STATIC_URL,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Simple JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
    # JWT creation and validation.
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    # Authentication Header
    "AUTH_HEADER_TYPES": (
        "Bearer",
    ),  # token must be sent in the Authorization header with the prefix Bearer
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # to strict security set ti true was in dock
    "ROTATE_REFRESH_TOKENS": False,  # a new refresh token is issued every time an access token is refreshed.
    "BLACKLIST_AFTER_ROTATION": True,  # old refresh tokens are blacklisted after rotation to prevent reuse.
    # tracking user activity not useful
    "UPDATE_LAST_LOGIN": True,
    # for frontend if store in cookies very important for local just delete
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_HTTP_ONLY": True,  # Prevents JavaScript from accessing the cookie
    "AUTH_COOKIE_SECURE": True,  # Ensures the cookie is only sent over HTTPS.
    "AUTH_COOKIE_SAMESITE": "None",  # Controls cross-site request behavior set to true but fronted
    # User Identification
    "USER_ID_FIELD": "id",  # tells the server which field in the database identifies the user
    "USER_ID_CLAIM": "user_id",  # where to find the user"s id in the jwt blabla
    # Token Classes
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# Application definition
INSTALLED_APPS = [
    # Built-in Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-Party Apps
    "corsheaders",
    "channels",
    "django.contrib.postgres",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework",
    # Custom Project Apps
    "project.core",
    "project.apps.pong",
    "project.apps.chat",
    "project.apps.custom_auth",
    "project.apps.users",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "project.asgi.application"
WSGI_APPLICATION = "project.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": "5432",
    }
}

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Ensure logs directory and log file exist
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOGS_DIR, "game_logs.log")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w"):
        pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "game_logs": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(os.path.dirname(__file__), "logs/game_logs.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "channels": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "game_logs": {
            "handlers": ["console", "game_logs"],
            "level": "DEBUG",
            "propagate": False,
        },
        "rest_api": {
            "handlers": ["console", "game_logs"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
