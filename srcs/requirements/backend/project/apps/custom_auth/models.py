import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def _create_user(self, name, password, **extra_fields):
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_user(self, name=None, password=None, **extra_fields):
        
        return self._create_user(name, email, password, **extra_fields)
    def create_superuser(self, name=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    is_online = models.BooleanField(default=False)
    avatar_url = models.CharField(max_length=200, blank=True, null=True)
    friends = models.JSONField(default=list, blank=True)
    objects = CustomUserManager()

    is_active = models.BooleanField(default=True)  # Required by Django
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(default=False)  # Required for superuser
    
    USERNAME_FIELD = 'name'

    REQUIRED_FIELDS = []

def __str__(self):
    self.name
