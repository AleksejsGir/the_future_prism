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


# apps/analytics/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from .models import Like
from .serializers import LikeSerializer
from apps.news.models import News

class LikeViewSet(viewsets.ModelViewSet):
    """
    API для управления лайками новостей.
    Позволяет создавать и удалять лайки.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        news_id = request.data.get('news')
        # Проверяем, что пользователь ещё не поставил лайк данной новости
        if Like.objects.filter(news_id=news_id, user=request.user).exists():
            return Response(
                {"detail": "Вы уже поставили лайк этой новости."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

class AnalyticsViewSet(viewsets.ViewSet):
    """
    API для получения агрегированной аналитики по новостям.
    Возвращает данные:
      - id новости
      - заголовок новости
      - количество просмотров (view_count из модели News)
      - количество лайков (подсчитанных через связь с Like)
    """
    def list(self, request):
        news_qs = News.objects.all().annotate(
            like_count=Count('likes')
        ).values('id', 'title', 'view_count', 'like_count')
        return Response(news_qs)
