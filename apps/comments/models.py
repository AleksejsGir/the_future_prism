# apps/comments/models.py
from django.db import models
from django.conf import settings

# Импортируем модель News из приложения news
# Если возникают ошибки импорта, убедись, что приложение news добавлено в INSTALLED_APPS
from apps.news.models import News

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', help_text="Новость, к которой относится комментарий")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', help_text="Автор комментария")
    content = models.TextField(help_text="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания комментария")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата последнего обновления")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', help_text="Родительский комментарий (для организации древовидной структуры)")
    is_approved = models.BooleanField(default=False, help_text="Одобрен ли комментарий модератором или AI")

    def __str__(self):
        return f"Комментарий от {self.author} к новости '{self.news}'"

    class Meta:
        ordering = ['created_at']
