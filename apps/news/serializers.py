# apps/news/serializers.py
from rest_framework import serializers
from .models import Category, News


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class NewsSerializer(serializers.ModelSerializer):
    # Можно выводить имя категории вместо её id, если нужно:
    # category = serializers.StringRelatedField()

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'published_date', 'category', 'view_count']
