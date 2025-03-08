# apps/news/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, NewsViewSet, toggle_favorite, favorite_news_list

# Создаем маршрутизатор для API-эндпоинтов
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    # Включаем маршруты из router
    path('', include(router.urls)),

    # Маршруты для избранных новостей
    path('favorites/', favorite_news_list, name='favorite_news_list'),
    path('favorites/toggle/<int:news_id>/', toggle_favorite, name='toggle_favorite'),
]

# Технические заметки
# - Добавлены маршруты для работы с избранными новостями
# - Проверить совместимость с многоязычными маршрутами
# - Убедиться в корректности работы API