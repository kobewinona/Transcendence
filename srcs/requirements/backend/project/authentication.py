import logging

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from project.apps.users.services import get_or_create_intra_user
from project.utils.auth import get_auth_provider
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger("rest_api")
User = get_user_model()


class JWTOrIntraAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "").strip()
        logger.debug(f"auth_header: { auth_header }")
        if not auth_header.startswith("Bearer "):
            return None

        access_token = auth_header.replace("Bearer ", "")
        logger.debug(f"access_token: { access_token }")

        auth_provider = get_auth_provider(access_token)

        if auth_provider == "internal":
            try:
                jwt_auth = JWTAuthentication()
                return jwt_auth.authenticate(request)
            except AuthenticationFailed as e:
                if "token_not_valid" in str(e):
                    raise AuthenticationFailed(
                        "Token has expired.", code="token_expired"
                    )
                logger.warning(f"JWT Authentication failed: {e}")

        intra_user = self.get_intra_user(access_token)

        if intra_user:
            return intra_user, None

        raise AuthenticationFailed("Invalid or expired token.", code="invalid_token")

    def get_intra_user(self, access_token):
        token_info_url = f"{settings.INTRA_URL}/oauth/token/info"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(token_info_url, headers=headers)
            response.raise_for_status()
            token_data = response.json()

            if token_data.get("expires_in_seconds", 0) > 0:
                intra_user_url = f"{settings.INTRA_URL}/v2/me"
                user_response = requests.get(intra_user_url, headers=headers)
                user_response.raise_for_status()
                intra_user_data = user_response.json()

                return get_or_create_intra_user(intra_user_data)

        except requests.RequestException:
            logger.error("Failed to validate token or fetch user from Intra.")

        return None
