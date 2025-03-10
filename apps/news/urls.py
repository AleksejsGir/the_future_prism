# apps/news/urls.py
from django.urls import path, include
from .views import NewsCategoryListView, NewsDetailView, toggle_favorite_view, favorite_news_list

urlpatterns = [
    # API включаем через include
    path('api/', include('apps.news.api.urls')),

    # Веб-маршруты (удаляем префикс 'news/' так как он будет добавлен через include)
    path('', NewsCategoryListView.as_view(), name='news_list'),
    path('<int:news_id>/', NewsDetailView.as_view(), name='news_detail'),
    path('favorites/', favorite_news_list, name='favorite_news_list'),
    path('favorites/toggle/<int:news_id>/', toggle_favorite_view, name='toggle_favorite'),
]
# Технические заметки
# - Добавлены маршруты для работы с избранными новостями
# - Проверить совместимость с многоязычными маршрутами
# - Убедиться в корректности работы API