from django.db import models
from .managers import IntraUserManager
from django.apps import apps
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# class IntraUser(models.Model):
#     objects = IntraUserManager()
#     id = models.BigIntegerField(primary_key=True)
#     email = models.EmailField(unique=True)
#     intra_login = models.CharField(max_length=8, unique=True)
#     avatar = models.CharField(max_length=100)
#     avatar_url = models.CharField(max_length=200, blank=True, null=True)
#     friends = models.JSONField(default=list, blank=True)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     is_anonymous = models.BooleanField(default=False)
#     is_authenticated = models.BooleanField(default=True)
#     USERNAME_FIELD = 'name'
#     REQUIRED_FIELDS = ['intra_login']
    
    
    
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