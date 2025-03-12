# apps/comments/services.py
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import Comment, CommentReaction
from apps.news.models import News


def get_comment_by_id(comment_id):
    """
    Получить комментарий по его ID
    """
    return get_object_or_404(Comment, id=comment_id)


def get_comments_for_news(news_id, sort_by='newest'):
    """
    Получить все комментарии для указанной новости с возможностью сортировки

    Параметры:
    - sort_by: тип сортировки ('newest', 'oldest', 'popular')
    """
    base_query = Comment.objects.filter(news_id=news_id, parent=None)

    if sort_by == 'oldest':
        # От старых к новым
        return base_query.order_by('created_at')
    elif sort_by == 'popular':
        # По популярности (больше всего лайков)
        return sorted(base_query, key=lambda c: c.reaction_score(), reverse=True)
    else:  # 'newest' или по умолчанию
        # От новых к старым
        return base_query.order_by('-created_at')


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
    """
    comments = Comment.objects.filter(is_approved=True)
    # Сортируем по количеству лайков (минус дизлайки)
    sorted_comments = sorted(comments, key=lambda c: c.reaction_score(), reverse=True)
    return sorted_comments[:limit]


def toggle_comment_reaction(user, comment_id, reaction_type):
    """
    Добавляет, изменяет или удаляет реакцию пользователя на комментарий.

    Параметры:
    - user: Пользователь, который оставляет реакцию
    - comment_id: ID комментария
    - reaction_type: Тип реакции ('like' или 'dislike')

    Возвращает:
    - tuple: (действие, новое_количество_лайков, новое_количество_дизлайков)
    - действие: 'added', 'changed', 'removed'
    """
    if not user.is_authenticated:
        raise ValidationError(_('Необходимо войти в систему для оценки комментариев'))

    if reaction_type not in [CommentReaction.LIKE, CommentReaction.DISLIKE]:
        raise ValidationError(_('Неверный тип реакции'))

    comment = get_comment_by_id(comment_id)

    # Проверяем, есть ли уже реакция от этого пользователя
    try:
        existing_reaction = CommentReaction.objects.get(comment=comment, user=user)

        # Если такая же реакция - удаляем её (снимаем лайк/дизлайк)
        if existing_reaction.like_type == reaction_type:
            existing_reaction.delete()
            action = 'removed'
        # Если другая реакция - меняем тип
        else:
            existing_reaction.like_type = reaction_type
            existing_reaction.save()
            action = 'changed'

    # Если реакции не было - создаем новую
    except CommentReaction.DoesNotExist:
        CommentReaction.objects.create(
            comment=comment,
            user=user,
            like_type=reaction_type
        )
        action = 'added'

    # Возвращаем текущее количество лайков и дизлайков
    return action, comment.like_count(), comment.dislike_count()