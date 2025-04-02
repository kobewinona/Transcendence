# noinspection PyUnresolvedReferences
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            )
        ],
    )

    username = serializers.CharField(
        required=True,
        min_length=2,
        error_messages={
            "required": "Username is required.",
            "min_length": "Username must be at least 2 characters long.",
        },
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        error_messages={
            "required": "Password is required.",
            "min_length": "Password must be at least 6 characters long.",
        },
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        if not re.search(r"[^A-Za-z0-9]", value):
            raise serializers.ValidationError(
                "Password must include at least one special character."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField()
