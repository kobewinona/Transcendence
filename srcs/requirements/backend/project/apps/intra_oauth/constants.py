import os

from django.conf import settings

APP_ENV = os.getenv("APP_ENV", "dev")

if APP_ENV == "production":
    REDIRECT_URI = "https://localhost/api/signin_intra/callback"
else:
    REDIRECT_URI = "http://localhost:8001/api/signin_intra/callback"

TOKEN_ENDPOINT = f"{settings.INTRA_URL}/oauth/token"
AUTHORIZE_ENDPOINT = f"{settings.INTRA_URL}/oauth/authorize"
