import logging
import os
import urllib.parse

import pyotp
import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from project.apps.users.services import get_or_create_intra_user
from project.utils.auth import get_auth_provider
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, OTPRequestSerializer, OTPVerifySerializer

from project.settings import secrets_backend

User = get_user_model()
REDIRECT_URI = os.getenv("REDIRECT_URI")
resend = secrets_backend.get("RESEND_API_KEY")
logger = logging.getLogger("auth_logs")


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


def generate_otp():
    totp = pyotp.TOTP(
        pyotp.random_base32(), interval=300
    )  # validity duration in seconds
    return totp.now()


def send_email(email, username, otp):
    url = "https://api.resend.com/emails"
    headers = {"Authorization": f"Bearer {resend}", "Content-Type": "application/json"}
    data = {
        "from": "Transcendence Team <otp@birgabon.me>",
        "to": [email],
        "subject": "Your Two-factor Authentication code | do not reply",
        "html": render_to_string(
            "emails/otp_email.html", {"username": username, "otp": otp}
        ),
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print("✓ Email sent successfully")
        else:
            print(f"✕ Failed to send email: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✕ Failed to send email: {str(e)}")


class GetOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)

        if user is None:
            return JsonResponse(
                {"error": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = generate_otp()
        cache.set(f"otp_{email}", otp, timeout=300)  # cache for 5 minutes
        send_email(user.email, user.username, otp)

        return Response(status=status.HTTP_200_OK)


class SignIn(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        received_otp = serializer.validated_data["otp"]
        stored_otp = cache.get(f"otp_{email}")

        if not stored_otp or received_otp != stored_otp:
            return JsonResponse(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        cache.delete(f"otp_{email}")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = JsonResponse(
            {"access_token": access_token}, status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            samesite="Lax",
        )

        return response


class RefreshTokens(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return JsonResponse(
                {"error": "Refresh token is missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = JsonResponse(
                {"access_token": access_token}, status=status.HTTP_200_OK
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                samesite="Lax",
            )
            return response

        except InvalidToken:
            return JsonResponse(
                {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )


class SignInIntra(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = secrets_backend.get("CLIENT_ID")

        params = urllib.parse.urlencode(
            {
                "client_id": client_id,
                "redirect_uri": REDIRECT_URI,
                "response_type": "code",
            }
        )

        auth_url = f"https://api.intra.42.fr/oauth/authorize?{params}"
        return HttpResponseRedirect(auth_url)


class SignInIntraCallback(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return HttpResponseBadRequest("Authorization code missing")

        data = {
            "client_id": secrets_backend.get("CLIENT_ID"),
            "client_secret": secrets_backend.get("CLIENT_SECRET"),
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
            "code": code,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            token_url = f"{settings.INTRA_URL}/oauth/token"
            response = requests.post(token_url, data=data, headers=headers)
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


class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return JsonResponse(
                {"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        auth_provider = get_auth_provider(refresh_token)

        if auth_provider == "internal":
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                logger.error(f"Failed to blacklist refresh token: {e}")
                return JsonResponse(
                    {"error": "Invalid or already used refresh token"}, status=400
                )

        # If it's an Intra token, we just remove it from cookies since we can't revoke it properly with intra
        response = JsonResponse({"message": "Signed out successfully"}, status=200)
        response.delete_cookie("refresh_token")

        return response
