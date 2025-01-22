from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

def _str_(self):
    self.username

    

