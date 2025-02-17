# core/urls.py

from django.contrib import admin
from django.urls import path, include
from .views import home, news_list, news_detail
from apps.users.views import (
    user_login, register_view, profile, edit_profile  # Добавляем edit_profile
)
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.conf import settings
from django.conf.urls.static import static

# Основные URL-маршруты проекта
urlpatterns = [
    # Административная панель Django
    path('admin/', admin.site.urls),

    # Главная страница и новости
    path('', home, name='home'),
    path('news/', news_list, name='news_list'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),

    # Аутентификация и управление профилем
    path('login/', user_login, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),  # Новый маршрут

    # Маршруты для сброса пароля
    path('password-reset/',
         PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    # API и дополнительные приложения
    path('tinymce/', include('tinymce.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/news/', include('apps.news.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

# Добавление обработки медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)