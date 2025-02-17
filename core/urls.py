# core/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home, news_list, news_detail
from apps.users.views import user_login, register_view, profile
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('news/', news_list, name='news_list'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),

    # Аутентификация
    path('login/', user_login, name='login'),
    path('register/', register_view, name='register'),  # веб-форма регистрации
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile, name='profile'),

    # Сброс пароля
    path('password-reset/',
         PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    # API URLs
    path('tinymce/', include('tinymce.urls')),
    path('api/users/', include('apps.users.urls')),  # API endpoints
    path('api/news/', include('apps.news.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)