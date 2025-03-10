# apps/users/api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserProfileAPIView, DeleteAvatarAPIView

urlpatterns = [
    # Аутентификация через JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API endpoints для пользователей
    path('register/', UserRegistrationView.as_view(), name='api_register'),
    path('profile/', UserProfileAPIView.as_view(), name='api_profile'),
    path('profile/avatar/delete/', DeleteAvatarAPIView.as_view(), name='api_delete_avatar'),
]