# apps/comments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _

from .models import Comment, CommentReaction
from apps.news.models import News
from .services import (
    get_comments_for_news,
    get_comment_replies,
    save_comment,
    approve_comment,
    delete_comment,
    toggle_comment_reaction
)  # Здесь не хватало закрывающей скобки


def comment_list(request, news_id):
    """
    Отображает список комментариев для статьи.
    """
    news = get_object_or_404(News, id=news_id)

    # Получаем тип сортировки из GET-параметров
    sort_by = request.GET.get('sort_by', 'newest')

    # Определяем, нужно ли показывать все комментарии
    show_all = request.GET.get('show_all') == 'true'

    # Получаем все комментарии для подсчета
    all_comments = Comment.objects.filter(news_id=news_id, parent=None)
    total_comments = all_comments.count()

    # По умолчанию показываем только первые 5 комментариев
    if not show_all and total_comments > 5:
        comments = get_comments_for_news(news_id, sort_by)[:5]
    else:
        comments = get_comments_for_news(news_id, sort_by)

    # Для каждого комментария устанавливаем user_reaction
    if request.user.is_authenticated:
        for comment in comments:
            comment.current_user_reaction = comment.user_reaction(request.user)
            # Также обрабатываем вложенные ответы
            for reply in comment.replies.all():
                reply.current_user_reaction = reply.user_reaction(request.user)

    context = {
        'news': news,
        'comments': comments,
        'total_comments': total_comments,
        'sort_by': sort_by,
        'show_all': show_all
    }

    # Если это AJAX-запрос, возвращаем только часть HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'comments/comment_list.html', context)

    return render(request, 'comments/comment_list.html', context)

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
        messages.success(request, _('Комментарий добавлен и ожидает проверки.'))
    else:
        messages.error(request, _('Комментарий не может быть пустым.'))

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
        messages.success(request, _('Комментарий удален.'))
        return redirect('news_detail', news_id=news_id)
    else:
        messages.error(request, _('У вас нет прав для удаления этого комментария.'))
        return redirect('news_detail', news_id=comment.news.id)


# apps/comments/views.py
@login_required
def toggle_reaction(request, comment_id):
    """
    Добавляет или удаляет реакцию (лайк/дизлайк) на комментарий.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': _('Необходимо авторизоваться')}, status=401)

    # Получаем reaction_type из POST данных
    reaction_type = request.POST.get('reaction_type')

    # Отладочная информация
    print(f"Received reaction request: comment_id={comment_id}")
    print(f"POST data: {request.POST}")
    print(f"Content-Type: {request.headers.get('Content-Type')}")
    print(f"Reaction type: {reaction_type}")

    try:
        # Проверяем наличие reaction_type и выполняем действие
        if not reaction_type:
            raise ValidationError(_('Отсутствует тип реакции в запросе'))

        action, likes_count, dislikes_count = toggle_comment_reaction(
            request.user, comment_id, reaction_type
        )

        # Получаем комментарий для редиректа
        comment = get_object_or_404(Comment, id=comment_id)

        # Добавляем сообщение об успешной операции
        if action == 'added':
            messages.success(request, _('Реакция добавлена'))
        elif action == 'changed':
            messages.success(request, _('Реакция изменена'))
        elif action == 'removed':
            messages.success(request, _('Реакция удалена'))

        # Всегда редиректим на страницу новости
        return redirect('news_detail', news_id=comment.news.id)

    except Exception as e:
        import traceback
        print(f"Error processing reaction: {str(e)}")
        print(traceback.format_exc())

        messages.error(request, str(e))

        # В случае ошибки тоже пытаемся редиректить на страницу новости
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            return redirect('news_detail', news_id=comment.news.id)
        except:
            # Если не удалось найти комментарий, редиректим на список новостей
            return redirect('news_list')