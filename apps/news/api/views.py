# apps/news/api/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Category, News
from ..services import increment_view_count, toggle_favorite
from .serializers import CategorySerializer, NewsSerializer, NewsDetailSerializer
from .permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для управления категориями новостей.

    Поддерживает стандартные операции CRUD и фильтрацию.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
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
    - Управление избранными новостями (добавление/удаление)
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'published_date']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'view_count', 'title']
    ordering = ['-published_date']  # Сортировка по умолчанию - от новых к старым

    def get_serializer_class(self):
        """Возвращает детальный сериализатор для retrieve."""
        if self.action == 'retrieve':
            return NewsDetailSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределяем метод retrieve для увеличения счетчика просмотров.
        """
        instance = self.get_object()
        increment_view_count(instance.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, pk=None):
        """
        Добавляет или удаляет новость из избранного пользователя.
        """
        try:
            is_favorite, message = toggle_favorite(request.user, pk)
            return Response({
                'success': True,
                'is_favorite': is_favorite,
                'message': message
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        """
        Возвращает список избранных новостей пользователя.
        """
        user = request.user
        favorites = user.favorites.all().order_by('-published_date')

        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)