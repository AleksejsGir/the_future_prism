# apps/news/api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Category, News

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий новостей."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей."""
    category_name = serializers.StringRelatedField(source='category')
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'short_description',
            'published_date', 'category', 'category_name',
            'view_count', 'image', 'is_favorite'
        ]

    def get_is_favorite(self, obj):
        """Проверяет, находится ли новость в избранном у пользователя."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj in request.user.favorites.all()
        return False


class NewsDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для отдельной новости."""
    category_name = serializers.StringRelatedField(source='category')
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'short_description',
            'published_date', 'category', 'category_name',
            'view_count', 'image', 'is_favorite'
        ]

    def get_is_favorite(self, obj):
        """Проверяет, находится ли новость в избранном у пользователя."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj in request.user.favorites.all()
        return False