# apps/comments/services.py
from django.shortcuts import get_object_or_404
from apps.comments.models import Comment
from apps.news.models import News

def get_comment_by_id(comment_id):
    """
    Получить комментарий по его ID
    """
    return get_object_or_404(Comment, id=comment_id)

def get_comments_for_news(news_id):
    """
    Получить все комментарии для указанной новости
    """
    return Comment.objects.filter(news_id=news_id, parent=None)

def get_comment_replies(comment_id):
    """
    Получить все ответы на комментарий
    """
    return Comment.objects.filter(parent_id=comment_id)

def save_comment(serializer, user):
    """
    Сохранить комментарий с указанием автора
    """
    return serializer.save(author=user)

def approve_comment(comment_id):
    """
    Одобрить комментарий
    """
    comment = get_comment_by_id(comment_id)
    comment.is_approved = True
    comment.save()
    return comment

def delete_comment(comment_id):
    """
    Удалить комментарий
    """
    comment = get_comment_by_id(comment_id)
    comment.delete()

def get_popular_comments(limit=5):
    """
    Получить популярные комментарии
    (в будущем можно добавить логику определения популярности)
    """
    return Comment.objects.filter(is_approved=True).order_by('-created_at')[:limit]