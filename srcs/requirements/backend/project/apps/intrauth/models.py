from django.db import models
from .managers import IntraUserManager
from django.apps import apps

class IntraUser(models.Model):
    objects = IntraUserManager()
    id = models.BigIntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    intra_login = models.CharField(max_length=8, unique=True)
    avatar = models.CharField(max_length=100)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['intra_login']
    
def is_authenticated(self, request):
    return True

    # def save(self, *args, **kwargs):
    #     if not self.email:
    #         self.email = f"{self.intra_login}@student.42.fr"
    #     super().save(*args, **kwargs)
    # def has_perm(self, perm, obj=None):
    #     return True
    # def has_module_perms(self, request):
    #     return True
    # def get_username(self):
    #     return self.intra_login
    # def __str__(self):
    #     return self.intra_login