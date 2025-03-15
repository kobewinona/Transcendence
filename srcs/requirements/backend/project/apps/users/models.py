from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    auth_provider = models.CharField(
        max_length=10,
        choices=[("internal", "Internal"), ("intra", "Intra")],
        default="internal",
    )
    intra_id = models.BigIntegerField(unique=True, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} ({self.auth_provider})"
