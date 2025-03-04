from django.db import models
from django.utils import timezone

class Category(models.Model):
    """
    Модель категории с поддержкой мультиязычности через django-modeltranslation.
    """
    name = models.CharField(max_length=255, unique=True, help_text="Название категории")
    description = models.TextField(blank=True, null=True, help_text="Описание категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class News(models.Model):
    """
    Модель новостей с поддержкой мультиязычности через django-modeltranslation.
    """
    title = models.CharField(max_length=255, help_text="Заголовок новости")
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="URL слаг (автогенерация из заголовка)")
    content = models.TextField(help_text="Содержимое новости")
    short_description = models.TextField(blank=True, null=True, help_text="Краткое описание новости")
    published_date = models.DateTimeField(default=timezone.now, help_text="Дата публикации")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news', help_text="Категория новости")
    view_count = models.PositiveIntegerField(default=0, help_text="Количество просмотров")
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)

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