from django.db import models
from django.utils import timezone

class Category(models.Model):
    """
    Модель категории с поддержкой мультиязычности через django-modeltranslation
    и добавлением Unicode-иконок.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Название категории",
        verbose_name="Название категории"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Описание категории",
        verbose_name="Описание категории"
    )
    # Новое поле для Unicode-иконки
    icon = models.CharField(
        max_length=10,  # Достаточно для emoji
        blank=True,
        null=True,
        help_text="Unicode-иконка для категории",
        verbose_name="Иконка"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class News(models.Model):
    """
    Модель новостей с поддержкой мультиязычности через django-modeltranslation.
    """
    title = models.CharField(
        max_length=255,
        help_text="Заголовок новости",
        verbose_name="Заголовок"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        help_text="URL слаг (автогенерация из заголовка)",
        verbose_name="URL слаг"
    )
    content = models.TextField(
        help_text="Содержимое новости",
        verbose_name="Содержимое"
    )
    short_description = models.TextField(
        blank=True,
        null=True,
        help_text="Краткое описание новости",
        verbose_name="Краткое описание"
    )
    published_date = models.DateTimeField(
        default=timezone.now,
        help_text="Дата публикации",
        verbose_name="Дата публикации"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='news',
        help_text="Категория новости",
        verbose_name="Категория"
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Количество просмотров",
        verbose_name="Просмотры"
    )
    image = models.ImageField(
        upload_to='news_images/',
        null=True,
        blank=True,
        help_text="Изображение для новости",
        verbose_name="Изображение"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            # Используем основное название для создания слага
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

# <!-- AI-TODO -->
# 1. Создать миграции после изменения модели
# 2. Обновить административную панель для отображения нового поля
# 3. Протестировать создание и редактирование категорий с иконками