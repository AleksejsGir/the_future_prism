# apps/users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,     # API регистрация
    user_login,               # Вход через веб-форму
    register_view,            # Веб-регистрация
    profile,                  # Просмотр профиля
    edit_profile,            # Редактирование профиля
    delete_avatar,           # Удаление аватара
    change_password,         # Изменение пароля
)

# Разделяем URL-паттерны на группы для лучшей организации
urlpatterns = [
    # API endpoints
    path('register/', UserRegistrationView.as_view(), name='api_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/password/', change_password, name='api_password_change'),

    # Веб-интерфейс аутентификации
    path('login/', user_login, name='login'),
    path('register/web/', register_view, name='register'),

    # Управление профилем
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/avatar/delete/', delete_avatar, name='delete_avatar'),
    path('profile/password/', change_password, name='password_change'),
]

# Примечания по URL-паттернам:
# 1. API endpoints используют /api/ префикс (настраивается в основном urls.py)
# 2. Веб-маршруты используют семантические имена
# 3. Маршруты профиля сгруппированы под /profile/
# 4. Все маршруты имеют уникальные имена для обратного разрешения URL
# 5. Маршрут смены пароля доступен как через API, так и через веб-интерфейс