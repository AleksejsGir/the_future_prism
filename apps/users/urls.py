# apps/users/urls.py
from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
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
    # Добавляем маршрут для выхода из системы
    path('logout/', LogoutView.as_view(
        template_name='registration/logged_out.html',
        next_page='home',
        http_method_names=['post', 'get'],
        extra_context={'title': 'Выход из системы'}
    ), name='logout'),

    # Маршруты для сброса пароля
    path('password-reset/', PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        success_url='/password-reset/done/',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        extra_context={'title': 'Сброс пароля'}
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
        extra_context={'title': 'Письмо отправлено'}
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/password-reset-complete/',
        extra_context={'title': 'Установка нового пароля'}
    ), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
        extra_context={'title': 'Пароль изменен'}
    ), name='password_reset_complete'),

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