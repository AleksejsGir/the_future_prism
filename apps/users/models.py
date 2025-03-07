# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя.
    Социальные сети и уведомления о новостях удалены по требованию заказчика.
    """
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

    # Добавляем поле для избранных новостей
    favorites = models.ManyToManyField(
        'news.News',
        related_name='favorited_by',
        blank=True,
        verbose_name=_('Избранные новости'),
        help_text=_('Новости, добавленные пользователем в избранное')
    )

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

# <!-- AI-TODO:
# 1. Удалено поле news_notifications
# 2. Проверить, нет ли зависимости в миграциях и формах
# 3. Обновить базу данных после удаления поля
# -->
