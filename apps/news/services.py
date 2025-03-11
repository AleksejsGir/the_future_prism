# apps/news/services.py
import os
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import logging

from .models import News, Category


def create_or_update_category(name, description=None, icon=None, category_id=None):
    """
    Создает новую или обновляет существующую категорию.

    Args:
        name (str): Название категории
        description (str, optional): Описание категории
        icon (str, optional): Unicode-иконка категории
        category_id (int, optional): ID существующей категории для обновления

    Returns:
        Category: Созданная или обновленная категория
    """
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            category.name = name
            category.description = description
            if icon:
                category.icon = icon
            category.save()
            return category
        except Category.DoesNotExist:
            raise ValidationError(_('Категория с указанным ID не существует'))
    else:
        return Category.objects.create(
            name=name,
            description=description,
            icon=icon
        )


def create_news(title, content, category, author=None, short_description=None, image=None):
    """
    Создает новую новость.

    Args:
        title (str): Заголовок новости
        content (str): Содержимое новости
        category (Category): Категория новости
        author (User, optional): Автор новости
        short_description (str, optional): Краткое описание
        image (File, optional): Изображение для новости

    Returns:
        News: Созданная новость
    """
    # Создаем слаг из заголовка
    slug = slugify(title)

    # Проверяем уникальность слага
    if News.objects.filter(slug=slug).exists():
        # Если слаг уже существует, добавляем к нему текущее время
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        slug = f"{slug}-{timestamp}"

    # Создаем новость
    news = News(
        title=title,
        content=content,
        short_description=short_description or '',
        category=category,
        slug=slug
    )

    # Если предоставлено изображение, сохраняем его
    if image:
        save_news_image(news, image)

    news.save()
    return news


def update_news(news_id, **kwargs):
    """
    Обновляет существующую новость.

    Args:
        news_id (int): ID новости для обновления
        **kwargs: Поля для обновления (title, content, category, etc.)

    Returns:
        News: Обновленная новость
    """
    try:
        news = News.objects.get(id=news_id)

        # Обновляем поля, если они предоставлены
        if 'title' in kwargs:
            news.title = kwargs['title']

            # Если заголовок изменился, возможно, стоит обновить слаг
            if kwargs.get('update_slug', False):
                news.slug = slugify(kwargs['title'])

                # Проверяем уникальность слага
                if News.objects.exclude(id=news_id).filter(slug=news.slug).exists():
                    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                    news.slug = f"{news.slug}-{timestamp}"

        if 'content' in kwargs:
            news.content = kwargs['content']

        if 'short_description' in kwargs:
            news.short_description = kwargs['short_description']

        if 'category' in kwargs:
            news.category = kwargs['category']

        if 'image' in kwargs and kwargs['image']:
            save_news_image(news, kwargs['image'])

        news.save()
        return news
    except News.DoesNotExist:
        raise ValidationError(_('Новость с указанным ID не существует'))


def save_news_image(news, image_file):
    """
    Сохраняет изображение для новости.

    Args:
        news (News): Объект новости
        image_file (File): Загруженное изображение

    Raises:
        ValidationError: Если формат файла не поддерживается или превышен размер
    """
    if not image_file:
        return

    # Проверяем размер файла (макс. 5 MB)
    if image_file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(_('Размер файла не должен превышать 5MB'))

    # Проверяем тип файла
    if not image_file.content_type.startswith('image/'):
        raise ValidationError(_('Пожалуйста, загрузите изображение'))

    # Проверяем, существует ли директория для сохранения изображений
    image_dir = os.path.join(settings.MEDIA_ROOT, 'news_images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Удаляем старое изображение, если оно существует
    if news.image:
        old_image_path = news.image.path
        if os.path.exists(old_image_path):
            os.remove(old_image_path)

    # Сохраняем новое изображение
    news.image = image_file


def increment_view_count(news_id):
    """
    Увеличивает счетчик просмотров новости.

    Args:
        news_id (int): ID новости

    Returns:
        int: Новое значение счетчика просмотров
    """
    # Используем F() для атомарного увеличения счетчика
    news = News.objects.filter(id=news_id)
    news.update(view_count=F('view_count') + 1)

    # Получаем обновленное значение
    updated_news = News.objects.get(id=news_id)
    return updated_news.view_count


def toggle_favorite(user, news_id):
    """
    Добавляет или удаляет новость из избранного пользователя.

    Args:
        user (User): Пользователь
        news_id (int): ID новости

    Returns:
        tuple: (bool, str) - (добавлено/удалено, сообщение)
        
    Raises:
        ValidationError: Если новость не найдена или возникла другая ошибка
    """
    if not user.is_authenticated:
        raise ValidationError(_('Необходимо войти в систему для работы с избранным'))
        
    try:
        news = News.objects.get(pk=news_id)
        
        # Проверяем, есть ли новость в избранном
        if news in user.favorites.all():
            # Если есть - удаляем
            user.favorites.remove(news)
            return False, _('Новость удалена из избранного')
        else:
            # Если нет - добавляем
            user.favorites.add(news)
            return True, _('Новость добавлена в избранное')

    except News.DoesNotExist:
        raise ValidationError(_('Новость не найдена'))
    except Exception as e:
        # Логируем необработанные исключения для дальнейшего анализа
        logger = logging.getLogger('django')
        logger.error(f'Ошибка при работе с избранным: {str(e)}')
        raise ValidationError(_('Произошла ошибка при обработке запроса'))