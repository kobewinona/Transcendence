import os

from django.conf import settings

REDIRECT_URI = os.getenv("REDIRECT_URI")

TOKEN_ENDPOINT = f"{settings.INTRA_URL}/oauth/token"
