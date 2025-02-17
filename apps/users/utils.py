from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import os


def validate_image_file(file):
    """
    Проверяет загружаемое изображение на соответствие требованиям.

    Args:
        file: UploadedFile объект

    Raises:
        ValidationError: если файл не соответствует требованиям
    """
    # Проверка размера файла
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            f'Размер файла не должен превышать {settings.MAX_UPLOAD_SIZE // (1024 * 1024)}MB'
        )

    # Проверка типа файла
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            'Поддерживаются только форматы: JPEG, PNG и GIF'
        )

    # Проверка размеров изображения
    image = Image.open(file)
    if (image.width > settings.MAX_IMAGE_DIMENSIONS['width'] or
            image.height > settings.MAX_IMAGE_DIMENSIONS['height']):
        raise ValidationError(
            f'Максимальный размер изображения: {settings.MAX_IMAGE_DIMENSIONS["width"]}x{settings.MAX_IMAGE_DIMENSIONS["height"]} пикселей'
        )


def process_avatar(file):
    """
    Обрабатывает загруженный аватар: изменяет размер и оптимизирует.

    Args:
        file: UploadedFile объект

    Returns:
        PIL.Image: обработанное изображение
    """
    image = Image.open(file)

    # Конвертируем в RGB, если изображение в другом формате
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGB')

    # Изменяем размер, сохраняя пропорции
    image.thumbnail((
        settings.AVATAR_DIMENSIONS['width'],
        settings.AVATAR_DIMENSIONS['height']
    ))

    # Если нужен квадратный аватар, обрезаем до квадрата
    if image.width != image.height:
        size = min(image.width, image.height)
        left = (image.width - size) // 2
        top = (image.height - size) // 2
        right = left + size
        bottom = top + size
        image = image.crop((left, top, right, bottom))

    return image


def save_avatar(user, file):
    """
    Сохраняет аватар пользователя с обработкой.

    Args:
        user: объект CustomUser
        file: UploadedFile объект
    """
    # Проверяем файл
    validate_image_file(file)

    # Обрабатываем изображение
    processed_image = process_avatar(file)

    # Формируем путь для сохранения
    filename = f'avatar_{user.id}{os.path.splitext(file.name)[1]}'
    filepath = os.path.join('avatars', filename)

    # Удаляем старый аватар, если он существует
    if user.avatar:
        old_avatar_path = user.avatar.path
        if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)

    # Сохраняем новый аватар
    processed_image.save(
        os.path.join(settings.MEDIA_ROOT, filepath),
        quality=85,  # немного сжимаем для оптимизации
        optimize=True
    )

    # Обновляем поле в модели
    user.avatar = filepath
    user.save(update_fields=['avatar'])