import logging
import os
import urllib.parse

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from project.apps.users.services import get_or_create_intra_user
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .constants import REDIRECT_URI, TOKEN_ENDPOINT, AUTHORIZE_ENDPOINT

resend = os.environ.get("RESEND_API_KEY")

User = get_user_model()

logger = logging.getLogger("rest_api")


class SignInIntra(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = os.getenv("CLIENT_ID")
        params = {
            "client_id": os.getenv("CLIENT_ID"),
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
        }
        oauth_url = f"{AUTHORIZE_ENDPOINT}?{urllib.parse.urlencode(params)}"
        print("Redirecting user to:", oauth_url)
        return redirect(oauth_url)


class SignInIntraCallback(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return HttpResponseBadRequest("Authorization code missing")

        data = {
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
            "code": code,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(TOKEN_ENDPOINT, data=data, headers=headers)
            response.raise_for_status()
            token_data = response.json()
            logger.debug(f"ⓘ Intra Token_data: { token_data }")

            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            logger.debug(f"ⓘ Intra Access_token: { access_token }")

            if not access_token:
                return HttpResponseBadRequest("Failed to get access token")

            intra_user_url = f"{settings.INTRA_URL}/v2/me"
            headers = {"Authorization": f"Bearer {access_token}"}

            intra_response = requests.get(intra_user_url, headers=headers)
            intra_response.raise_for_status()
            intra_user_data = intra_response.json()
            logger.debug(f"ⓘ Intra User Info: {intra_user_data}")

            get_or_create_intra_user(intra_user_data)

            access_token_param = {
                "access_token": access_token,
            }

            response = redirect(
                f"{settings.APP_URL}/signin?{urllib.parse.urlencode(access_token_param)}"
            )
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
            )

            return response

        except requests.RequestException as e:
            return HttpResponseBadRequest(f"OAuth token request failed: {str(e)}")
