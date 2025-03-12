# apps/comments/api/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.comments.models import Comment
from apps.comments.api.serializers import CommentSerializer
from apps.comments.services import save_comment

class CommentViewSet(viewsets.ModelViewSet):
    """
    API для управления комментариями.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Используем сервисный слой для создания комментария
        save_comment(serializer, self.request.user)