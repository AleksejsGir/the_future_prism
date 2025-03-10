# apps/news/urls.py
from django.urls import path, include
from .views import (
    NewsCategoryListView, NewsDetailView,
    toggle_favorite_view, favorite_news_list
)

urlpatterns = [
    # API включаем через include
    path('api/', include('apps.news.api.urls')),

    # Веб-маршруты
    path('news/', NewsCategoryListView.as_view(), name='news_list'),
    path('news/<int:news_id>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/favorites/', favorite_news_list, name='favorite_news_list'),
    path('news/favorites/toggle/<int:news_id>/', toggle_favorite_view, name='toggle_favorite'),
]

# Технические заметки
# - Добавлены маршруты для работы с избранными новостями
# - Проверить совместимость с многоязычными маршрутами
# - Убедиться в корректности работы API