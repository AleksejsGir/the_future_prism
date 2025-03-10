# apps/users/services.py
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import CustomUser


def save_avatar(user, avatar_file):
    """
    Обработка и сохранение аватара пользователя.

    Args:
        user (CustomUser): Объект пользователя
        avatar_file (File): Загруженное изображение аватара

    Returns:
        str: URL-путь к аватару

    Raises:
        ValidationError: Если формат файла не поддерживается или превышен размер
    """
    if not avatar_file:
        return None

    # Проверяем размер файла (макс. 5 MB)
    if avatar_file.size > 5 * 1024 * 1024:
        raise ValidationError(_('Размер файла не должен превышать 5MB'))

    # Проверяем тип файла
    if not avatar_file.content_type.startswith('image/'):
        raise ValidationError(_('Пожалуйста, загрузите изображение'))

    # Проверяем, существует ли директория для сохранения аватаров
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)

    # Удаляем старый аватар, если он существует
    if user.avatar:
        old_avatar_path = user.avatar.path
        if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)

    # Сохраняем новый аватар
    user.avatar = avatar_file
    user.save(update_fields=['avatar'])

    return user.get_avatar_url()


def toggle_user_favorite(user, news_item):
    """
    Добавляет или удаляет новость из избранного пользователя.

    Args:
        user (CustomUser): Объект пользователя
        news_item (News): Объект новости

    Returns:
        bool: True, если новость добавлена в избранное, False - если удалена
    """
    if news_item in user.favorites.all():
        user.favorites.remove(news_item)
        return False
    else:
        user.favorites.add(news_item)
        return True