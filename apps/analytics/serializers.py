# apps/analytics/serializers.py
from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'news', 'user', 'created_at']
        read_only_fields = ['created_at', 'user']

    def create(self, validated_data):
        # Автоматически устанавливаем пользователя из запроса
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
