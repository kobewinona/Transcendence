import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

from .constants import REFRESH_TOKEN_LIFETIME_DAYS, ACCESS_TOKEN_LIFETIME_MINUTES
from .utils.logger import CustomFormatter

from project.load_env_file import load_env_file

# -----------------------------------------------
# 🏗️ PROJECT BASE SETTINGS
# -----------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
APP_ENV_MODE = os.getenv("APP_ENV_MODE", "production")  # "development" or "production"
APP_URL = os.getenv("APP_URL")  # Frontend URL
WSS_URL = os.getenv("WSS_URL")  # Frontend Socket URL
INTRA_URL = "https://api.intra.42.fr"
AUTH_USER_MODEL = "users.CustomUser"

# Load environment variables
load_dotenv()

# -----------------------------------------------
# 📂 STATIC & MEDIA FILES
# -----------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = "/usr/src/app/staticfiles"

# -----------------------------------------------
# 🌎 INTERNATIONALIZATION
# -----------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------
# 🔑 CREDENTIAL FROM VAULT
# -----------------------------------------------

BACKEND_ENV_PATH = "/usr/src/app/vault/secrets/backend/.env.key"
POSTGRES_ENV_PATH = "/usr/src/app/vault/secrets/postgres/.env.db"

secrets_backend = load_env_file(BACKEND_ENV_PATH)
secrets_postgres = load_env_file(POSTGRES_ENV_PATH)

# -----------------------------------------------
# 🔒 SECURITY SETTINGS
# -----------------------------------------------

# Secret Key (⚠️ Should be set in a secure way in production)
SECRET_KEY = secrets_backend.get("SECRET_KEY")

# Debug mode (ON in development, OFF in production)
DEBUG = APP_ENV_MODE == "development"

# Trusted Proxies (when using reverse proxy)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Enforce secure cookies in production
SESSION_COOKIE_SECURE = APP_ENV_MODE == "production"
CSRF_COOKIE_SECURE = APP_ENV_MODE == "production"

ALLOWED_HOSTS = ["backend", "localhost", INTRA_URL]

# -----------------------------------------------
# 🌍 CORS & CSRF CONFIGURATION
# -----------------------------------------------

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [APP_URL]
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrf-token",
    "x-requested-with",
]

# Content Security Policy (CSP)
CSP_CONNECT_SRC = (
    "'self'",
    APP_URL,  # Allow frontend connections
    WSS_URL,  # Allow frontend socket connections
    INTRA_URL,
)

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    APP_URL,
    INTRA_URL,
]

# -----------------------------------------------
# 🔑 AUTHENTICATION & PASSWORD SECURITY
# -----------------------------------------------

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------
# 🔑 JWT AUTHENTICATION SETTINGS
# -----------------------------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),  # Token prefix: "Bearer <token>"
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_SECURE": True,
    "AUTH_COOKIE_SAMESITE": "None",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# -----------------------------------------------
# ⚙️ APPLICATION CONFIGURATION
# -----------------------------------------------

INSTALLED_APPS = [
    # Django Built-in Apps
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
    "project.apps.oauth",
    "project.apps.users",
    "project.apps.tournaments",
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


# -----------------------------------------------
# 🛢️ DATABASE CONFIGURATION
# -----------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": secrets_postgres.get("POSTGRES_DB"),
        "USER": secrets_postgres.get("POSTGRES_USER"),
        "PASSWORD": secrets_postgres.get("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": "5432",
    }
}

# -----------------------------------------------
# ⚡ DJANGO CHANNELS (WebSockets)
# -----------------------------------------------

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# -----------------------------------------------
# ⚙️ REST FRAMEWORK SETTINGS
# -----------------------------------------------

REST_FRAMEWORK = {
    "STATIC_URL": STATIC_URL,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "project.authentication.JWTOrIntraAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "EXCEPTION_HANDLER": "project.utils.exceptions.custom_exception_handler",
}

# -----------------------------------------------
# 🏗️ DEFAULT CONFIGURATIONS
# -----------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------
# 📢 LOGGING CONFIGURATION
# -----------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "colored": {
            "()": CustomFormatter,
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if APP_ENV_MODE == "development" else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "channels": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "game_logs": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "auth_logs": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "fast-reload_logs": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "tournaments_logs": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
}
