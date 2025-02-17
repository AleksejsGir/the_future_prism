# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя.
    Наследуется от AbstractUser для сохранения базового функционала Django.
    """
    # Основные поля профиля
    bio = models.TextField(
        verbose_name=_('О себе'),
        blank=True,
        null=True,
        help_text=_('Краткая информация о пользователе')
    )

    avatar = models.ImageField(
        verbose_name=_('Аватар'),
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text=_('Изображение профиля пользователя')
    )

    email_notifications = models.BooleanField(
        verbose_name=_('Уведомления на email'),
        default=True,
        help_text=_('Получать уведомления на email')
    )

    # Дополнительные поля для отслеживания активности
    last_activity = models.DateTimeField(
        verbose_name=_('Последняя активность'),
        auto_now=True,
        help_text=_('Время последней активности пользователя')
    )

    # Добавим поле для избранных статей позже, когда создадим модель News
    # favorites = models.ManyToManyField(
    #     'news.News',
    #     verbose_name=_('Избранные статьи'),
    #     related_name='favorited_by',
    #     blank=True
    # )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        Если не указано, возвращает имя пользователя.
        """
        full_name = super().get_full_name()
        return full_name if full_name else self.username

    def get_avatar_url(self):
        """
        Возвращает URL аватара пользователя.
        Если аватар не загружен, возвращает None.
        """
        return self.avatar.url if self.avatar else None