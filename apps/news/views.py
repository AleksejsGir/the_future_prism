# apps/news/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category, News
from .serializers import CategorySerializer, NewsSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для управления категориями новостей.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class NewsViewSet(viewsets.ModelViewSet):
    """
    API для управления новостями.
    При получении детальной информации увеличиваем счётчик просмотров.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def retrieve(self, request, *args, **kwargs):
        # Получаем объект новости
        instance = self.get_object()
        # Увеличиваем счетчик просмотров
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
