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


# apps/news/api/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': _('Необходимо войти в систему для работы с избранным')
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            is_favorite, message = toggle_favorite(request.user, pk)
            return Response({
                'success': True,
                'is_favorite': is_favorite,
                'message': message
            })
        except ValidationError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Логируем необработанные исключения
            import logging
            logger = logging.getLogger('django')
            logger.error(f'API ошибка в toggle_favorite: {str(e)}')
            
            return Response({
                'success': False,
                'message': _('Произошла ошибка при обработке запроса')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        """
        Возвращает список избранных новостей пользователя.
        """
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'message': _('Необходимо войти в систему для просмотра избранного')
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            user = request.user
            favorites = user.favorites.all().order_by('-published_date')

            page = self.paginate_queryset(favorites)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(favorites, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Логируем необработанные исключения
            import logging
            logger = logging.getLogger('django')
            logger.error(f'API ошибка в favorites: {str(e)}')
            
            return Response({
                'success': False,
                'message': _('Произошла ошибка при получении избранных новостей')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)