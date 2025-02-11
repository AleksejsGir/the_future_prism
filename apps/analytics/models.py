# apps/analytics/models.py
from django.db import models
from django.conf import settings
from apps.news.models import News

class Like(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text="Новость, к которой поставлен лайк"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text="Пользователь, поставивший лайк"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время постановки лайка")

    class Meta:
        unique_together = ('news', 'user')  # каждый пользователь может лайкнуть новость только один раз
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} лайкнул {self.news}"
