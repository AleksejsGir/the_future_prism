# core/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home, NewsListView, news_detail
from apps.users.views import (
    user_login, register_view, profile, edit_profile, delete_avatar
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
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),

    # Аутентификация и управление профилем
    path('login/', user_login, name='login'),
    path('register/', register_view, name='register'),

    # Обновленная настройка выхода из системы
    path('logout/',
         LogoutView.as_view(
             template_name='registration/logged_out.html',  # Шаблон для страницы выхода
             next_page='home',  # Перенаправление после выхода
             http_method_names=['post', 'get'],  # Разрешаем оба метода
             extra_context={'title': 'Выход из системы'}  # Дополнительный контекст
         ),
         name='logout'
         ),

    # Управление профилем пользователя
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/avatar/delete/', delete_avatar, name='delete_avatar'),

    # Маршруты для сброса пароля с улучшенными настройками
    path('password-reset/',
         PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             success_url='/password-reset/done/',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             extra_context={'title': 'Сброс пароля'}
         ),
         name='password_reset'),

    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html',
             extra_context={'title': 'Письмо отправлено'}
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/password-reset-complete/',
             extra_context={'title': 'Установка нового пароля'}
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html',
             extra_context={'title': 'Пароль изменен'}
         ),
         name='password_reset_complete'),

    # API и дополнительные приложения
    path('tinymce/', include('tinymce.urls')),

    # API endpoints с версионированием
    path('api/v1/', include([
        path('users/', include('apps.users.urls')),
        path('news/', include('apps.news.urls')),
        path('comments/', include('apps.comments.urls')),
        path('analytics/', include('apps.analytics.urls')),
    ])),
]

# Настройка обработки медиафайлов в режиме разработки
if settings.DEBUG:
    # Добавляем обработку медиафайлов
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Добавляем Django Debug Toolbar если он установлен
    try:
        import debug_toolbar

        urlpatterns.append(
            path('__debug__/', include(debug_toolbar.urls))
        )
    except ImportError:
        pass  # Debug Toolbar не установлен