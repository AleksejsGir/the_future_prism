# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя.
    Наследуется от AbstractUser для сохранения базового функционала Django.
    """
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Краткая информация о пользователе"
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username