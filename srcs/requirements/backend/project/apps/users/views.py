import logging

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from project.apps.users.serializers import UserSerializer
from project.authentication import JWTOrIntraAuthentication
from project.utils.auth import get_auth_provider
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

logger = logging.getLogger("rest_api")


class UserInfo(APIView):
    authentication_classes = [JWTOrIntraAuthentication]
    permission_classes = [IsAuthenticated]

    def fetch_intra_user_info(self, access_token):
        intra_user_url = f"{settings.INTRA_URL}/v2/me"

        if access_token.startswith("Bearer "):
            access_token = access_token.replace("Bearer ", "").strip()

        headers = {"Authorization": f"Bearer {access_token}"}

        logger.debug(f"headers: { headers }")
        logger.debug(f"intra_user_url: { intra_user_url }")

        try:
            response = requests.get(intra_user_url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            raise AuthenticationFailed("Failed to retrieve user info from Intra.")

    def get(self, request):
        logger.debug(f"request: { request }")
        access_token = request.headers.get("Authorization", "").strip()
        logger.debug(f"access_token: { access_token }")

        if not access_token:
            raise AuthenticationFailed("No access token provided.")

        auth_provider = get_auth_provider(access_token)
        logger.debug(f"auth_provider: { auth_provider }")

        if auth_provider == "internal":
            user = request.user
            return Response(UserSerializer(user).data, status=200)

        elif auth_provider == "intra":
            intra_user = self.fetch_intra_user_info(access_token)

            # Optionally, update user in our DB to sync data
            user, created = User.objects.update_or_create(
                intra_id=intra_user["id"],
                defaults={
                    "username": intra_user["login"],
                    "email": intra_user["email"],
                    "intra_avatar": intra_user["image"]["link"],
                },
            )

            return Response(UserSerializer(user).data, status=200)
