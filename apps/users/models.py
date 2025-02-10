# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True, help_text="Краткая информация о пользователе")

    def __str__(self):
        return self.username
