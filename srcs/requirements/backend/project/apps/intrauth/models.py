from django.db import models
from .managers import IntraUserManager
from django.apps import apps
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
    
class CustomUser(AbstractUser):
    # Traditional
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)  # Optional
    password = models.CharField(max_length=128, blank=True, null=True)  # Nullable for OAuth users

    #  42 Intra
    objects = IntraUserManager()
    intra_id = models.BigIntegerField(unique=True, blank=True, null=True)
    intra_login = models.CharField(max_length=8, unique=True, blank=True, null=True)
    intra_avatar = models.URLField(max_length=200, blank=True, null=True)

    # Additional fields (common to all users)
    is_online = models.BooleanField(default=False)
    friends = models.JSONField(default=list, blank=True)

    # name as the primary identifier
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 
    
def is_authenticated(self, request):
    return True