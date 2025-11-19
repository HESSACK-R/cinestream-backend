# cinestream\backend\users\models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telegram_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username
