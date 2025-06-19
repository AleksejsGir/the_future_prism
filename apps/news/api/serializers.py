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
        if not request or not request.user.is_authenticated:
            return False
            
        try:
            return obj in request.user.favorites.all()
        except Exception:
            # В случае ошибки возвращаем False вместо поломки API
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
        if not request or not request.user.is_authenticated:
            return False
            
        try:
            return obj in request.user.favorites.all()
        except Exception:
            # В случае ошибки возвращаем False вместо поломки API
            return False