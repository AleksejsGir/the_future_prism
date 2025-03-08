# apps/news/views.py
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.shortcuts import render
from .models import Category, News
from .serializers import CategorySerializer, NewsSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для управления категориями новостей.
    Поддерживает стандартные операции CRUD.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class NewsViewSet(viewsets.ModelViewSet):
    """
    API для управления новостями.
    Поддерживает:
    - Фильтрацию по категории и дате публикации
    - Поиск по заголовку и содержимому
    - Сортировку по различным полям
    - Автоматическое увеличение счётчика просмотров при детальном просмотре
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'published_date']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'view_count', 'title']
    ordering = ['-published_date']  # Сортировка по умолчанию - от новых к старым

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределяем метод retrieve для увеличения счетчика просмотров.
        Используем update_fields для оптимизации запроса к БД.
        """
        instance = self.get_object() # Получаем объект новости
        instance.view_count += 1 # Увеличиваем счетчик просмотров
        instance.save(update_fields=['view_count']) # Сохраняем изменения
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@login_required
def toggle_favorite(request, news_id):
    """
    Добавляет или удаляет новость из избранного.

    Если новость уже в избранном - удаляет её.
    Если новости нет в избранном - добавляет её.
    Работает как с GET, так и с POST запросами для совместимости.
    """
    try:
        news = News.objects.get(pk=news_id)
        user = request.user

        # Проверяем, есть ли новость в избранном
        if news in user.favorites.all():
            # Если есть - удаляем
            user.favorites.remove(news)
            is_favorite = False
            message = _('Новость удалена из избранного')
        else:
            # Если нет - добавляем
            user.favorites.add(news)
            is_favorite = True
            message = _('Новость добавлена в избранное')

        # Если это AJAX-запрос, возвращаем JSON-ответ
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_favorite': is_favorite,
                'message': message
            })

        # Иначе добавляем сообщение и делаем редирект
        messages.success(request, message)
        return redirect('news_detail', news.id)

    except News.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': _('Новость не найдена')
            }, status=404)
        messages.error(request, _('Новость не найдена'))
        return redirect('news_list')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
        messages.error(request, str(e))
        return redirect('news_list')


@login_required
def favorite_news_list(request):
    """
    Отображает список избранных новостей пользователя.

    Требует аутентификации. Возвращает страницу со списком
    всех новостей, добавленных пользователем в избранное.
    """
    user = request.user
    # Получаем избранные новости пользователя
    news_list = user.favorites.all().order_by('-published_date')

    context = {
        'news_list': news_list,
        'title': _('Избранные новости'),
    }

    return render(request, 'news/favorites_list.html', context)