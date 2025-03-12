# apps/comments/api/serializers.py
from rest_framework import serializers
from apps.comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    # Для отображения древовидной структуры можно добавить поле для дочерних комментариев
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'news',
            'author',
            'content',
            'created_at',
            'updated_at',
            'parent',
            'is_approved',
            'replies'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_approved', 'replies']

    def get_replies(self, obj):
        # Рекурсивно получаем дочерние комментарии
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []