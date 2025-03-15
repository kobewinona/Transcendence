# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            )
        ]
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def create(validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)  # Create a user instance without saving yet
        user.set_password(password)  # Hash the password
        user.save()
        return user


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.CharField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    otp = serializers.CharField()
