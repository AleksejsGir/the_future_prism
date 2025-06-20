# Copyright 2024-2025 Aleksejs Giruckis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# apps/news/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
import logging

from .models import News, Category
from .services import toggle_favorite, increment_view_count


class NewsCategoryListView(ListView):
    """
    Отображает список новостей с возможностью фильтрации по категориям.
    """
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 9  # Количество новостей на странице

    def get_queryset(self):
        """Возвращает отфильтрованный список новостей."""
        queryset = News.objects.all().order_by('-published_date')

        # Фильтрация по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Поиск по запросу
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | \
                       queryset.filter(content__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в контекст."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class NewsDetailView(DetailView):
    """
    Отображает детальную информацию о новости.
    """
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    pk_url_kwarg = 'news_id'

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в контекст."""
        context = super().get_context_data(**kwargs)

        # Добавляем информацию о категориях
        context['categories'] = Category.objects.all()

        # Проверяем, находится ли новость в избранном
        user = self.request.user
        if user.is_authenticated:
            context['is_favorite'] = self.object in user.favorites.all()
        else:
            context['is_favorite'] = False

        # Добавляем комментарии к новости
        # Получаем только корневые комментарии (без родителя)
        context['comments'] = self.object.comments.filter(parent=None).order_by('-created_at')

        # Добавляем похожие новости из той же категории
        context['similar_news'] = News.objects.filter(
            category=self.object.category
        ).exclude(
            id=self.object.id
        ).order_by('-published_date')[:3]

        return context

    def get(self, request, *args, **kwargs):
        """Увеличиваем счетчик просмотров и возвращаем страницу."""
        response = super().get(request, *args, **kwargs)
        increment_view_count(self.object.id)
        return response


@login_required
def toggle_favorite_view(request, news_id):
    """
    Добавляет или удаляет новость из избранного.
    """
    if not request.user.is_authenticated:
        messages.error(request, _('Необходимо войти в систему для работы с избранным'))
        return redirect('login')
        
    try:
        is_favorite, message = toggle_favorite(request.user, news_id)

        # Если это AJAX-запрос, возвращаем JSON-ответ
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_favorite': is_favorite,
                'message': message
            })

        # Иначе добавляем сообщение и делаем редирект
        messages.success(request, message)
        # Редирект на предыдущую страницу, если возможно
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('news_detail', news_id)

    except ValidationError as e:
        # Более детальная обработка ошибок валидации
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)  # Используем 400 Bad Request вместо 404
        messages.error(request, str(e))
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('news_list')

    except Exception as e:
        # Логируем необработанные исключения
        logger = logging.getLogger('django')
        logger.error(f'Необработанная ошибка в toggle_favorite_view: {str(e)}')
        
        # Возвращаем понятное пользователю сообщение
        error_message = _('Произошла ошибка при обработке запроса')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': error_message
            }, status=500)
        messages.error(request, error_message)
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('news_list')


@login_required
def favorite_news_list(request):
    """
    Отображает список избранных новостей пользователя.
    """
    user = request.user
    news_list = user.favorites.all().order_by('-published_date')

    context = {
        'news_list': news_list,
        'title': _('Избранные новости'),
        'categories': Category.objects.all(),
    }

    return render(request, 'news/favorites_list.html', context)