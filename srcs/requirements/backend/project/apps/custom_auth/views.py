import os
import pyotp
import requests
import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.template.loader import render_to_string
from project.constants import REFRESH_TOKEN_LIFETIME_DAYS

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, OTPRequestSerializer, OTPVerifySerializer

resend = os.environ.get("RESEND_API_KEY")
User = get_user_model()

logger = logging.getLogger("rest_api")


class SignUp(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]

        try:
            user = User.objects.get(username=username)
            otp = generate_otp()
            cache.set(
                f"otp_{username}", otp, timeout=300
            )  # caching duration in seconds

            send_email(user.email, username, otp)

            return Response(
                {"otp": otp}, status=status.HTTP_200_OK
            )  # TODO remove res body after development
        except User.DoesNotExist:
            return Response(
                {"detail": "User with this username does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignIn(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        logger.debug(f"username: { username }")
        received_otp = serializer.validated_data["otp"]
        stored_otp = cache.get(f"otp_{username}")
        logger.debug(f"received_otp: { received_otp }")
        logger.debug(f"stored_otp: { stored_otp }")

        if not stored_otp or received_otp != stored_otp:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        cache.delete(f"otp_{username}")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({"access_token": access_token}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
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
            return Response(
                {"error": "Refresh token is missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response(
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
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )


class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token missing"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"error": "Invalid or already used refresh token"}, status=400
            )

        response = Response({"message": "Signed out successfully"}, status=200)
        response.delete_cookie("refresh_token")

        return response
