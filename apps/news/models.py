# apps/news/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Название категории")
    description = models.TextField(blank=True, null=True, help_text="Описание категории")

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255, help_text="Заголовок новости")
    content = models.TextField(help_text="Содержимое новости")
    published_date = models.DateTimeField(auto_now_add=True, help_text="Дата публикации")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news', help_text="Категория новости")
    view_count = models.PositiveIntegerField(default=0, help_text="Количество просмотров")

    def __str__(self):
        return self.title
