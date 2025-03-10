# apps/users/api/views.py
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CustomUser
from ..services import save_avatar, toggle_user_favorite
from .serializers import UserRegistrationSerializer, UserProfileSerializer


class UserRegistrationView(generics.CreateAPIView):
    """API для регистрации пользователей."""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """API для получения и обновления профиля пользователя."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Обработка аватара, если он есть в запросе
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            try:
                save_avatar(instance, avatar_file)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)


class DeleteAvatarAPIView(APIView):
    """API для удаления аватара пользователя."""
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        if user.avatar:
            user.avatar.delete(save=False)
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'У пользователя нет аватара'}, status=status.HTTP_404_NOT_FOUND)