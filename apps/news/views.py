# apps/news/views.py
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)