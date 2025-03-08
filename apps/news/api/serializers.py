# apps/news/api/serializers.py

from rest_framework import serializers
from ..models import Category, News


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий новостей."""

    class Meta:
        model = Category
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для новостей."""

    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('view_count',)