# apps/news/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, NewsViewSet

# Создаем маршрутизатор для API-эндпоинтов
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    # Включаем маршруты из router
    path('', include(router.urls)),
]