# apps/comments/models.py
from django.db import models
from django.conf import settings
from apps.news.models import News


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments',
                             help_text="Новость, к которой относится комментарий")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments',
                               help_text="Автор комментария")
    content = models.TextField(help_text="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания комментария")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата последнего обновления")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                               help_text="Родительский комментарий (для организации древовидной структуры)")
    is_approved = models.BooleanField(default=False, help_text="Одобрен ли комментарий модератором или AI")

    # Добавим методы для работы с лайками
    def like_count(self):
        """Возвращает количество лайков комментария"""
        return self.likes.filter(like_type=CommentReaction.LIKE).count()

    def dislike_count(self):
        """Возвращает количество дизлайков комментария"""
        return self.likes.filter(like_type=CommentReaction.DISLIKE).count()

    def reaction_score(self):
        """Возвращает общий рейтинг (лайки - дизлайки)"""
        return self.like_count() - self.dislike_count()

    def user_reaction(self, user):
        """Возвращает реакцию пользователя на комментарий"""
        if not user.is_authenticated:
            return None
        try:
            return self.likes.get(user=user).like_type
        except CommentReaction.DoesNotExist:
            return None

    def __str__(self):
        return f"Комментарий от {self.author} к новости '{self.news}'"

    class Meta:
        ordering = ['created_at']


class CommentReaction(models.Model):
    """Модель для хранения реакций (лайков/дизлайков) на комментарии"""
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_TYPES = [
        (LIKE, 'Лайк'),
        (DISLIKE, 'Дизлайк'),
    ]

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_reactions')
    like_type = models.CharField(max_length=10, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
        verbose_name = 'Реакция на комментарий'
        verbose_name_plural = 'Реакции на комментарии'

    def __str__(self):
        return f"{self.get_like_type_display()} от {self.user} на комментарий {self.comment.id}"