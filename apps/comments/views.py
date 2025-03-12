# apps/comments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.comments.models import Comment
from apps.news.models import News
from apps.comments.services import (
    get_comments_for_news,
    get_comment_replies,
    save_comment,
    approve_comment,
    delete_comment
)


def comment_list(request, news_id):
    """
    Отображает список комментариев для статьи.
    """
    news = get_object_or_404(News, id=news_id)
    comments = get_comments_for_news(news_id)

    return render(request, 'comments/comment_list.html', {
        'news': news,
        'comments': comments
    })


@login_required
@require_POST
def add_comment(request, news_id):
    """
    Добавляет новый комментарий к статье.
    """
    news = get_object_or_404(News, id=news_id)
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')

    if content:
        comment = Comment(
            news=news,
            author=request.user,
            content=content
        )

        if parent_id:
            comment.parent_id = parent_id

        comment.save()
        messages.success(request, 'Комментарий добавлен и ожидает проверки.')
    else:
        messages.error(request, 'Комментарий не может быть пустым.')

    return redirect('news_detail', news_id=news_id)


@login_required
def delete_comment_view(request, comment_id):
    """
    Удаляет комментарий.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    # Проверяем, что пользователь является автором комментария или администратором
    if request.user == comment.author or request.user.is_staff:
        news_id = comment.news.id
        delete_comment(comment_id)
        messages.success(request, 'Комментарий удален.')
        return redirect('news_detail', news_id=news_id)
    else:
        messages.error(request, 'У вас нет прав для удаления этого комментария.')
        return redirect('news_detail', news_id=comment.news.id)