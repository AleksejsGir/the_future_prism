# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from .views import home, NewsListView, news_detail, about_view, contact_view

# Базовые маршруты без префикса языка
urlpatterns = [
    # Маршрут для переключения языков
    path('i18n/', include('django.conf.urls.i18n')),
]

# Многоязычные маршруты с префиксом языка
urlpatterns += i18n_patterns(
    # Административная панель Django
    path('admin/', admin.site.urls),

    # Главная страница и новости
    path('', home, name='home'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),

    # Страницы "О проекте" и "Контакты"
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),

    # Маршруты пользователей
    path('', include('apps.users.urls')),

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),

    # API endpoints с версионированием
    path('api/v1/', include([
        path('users/', include('apps.users.api.urls')),
        path('news/', include('apps.news.api.urls')),
        path('comments/', include('apps.comments.urls')),
        path('analytics/', include('apps.analytics.urls')),
    ])),

    # Важно! Устанавливаем prefix_default_language в True
    prefix_default_language=True
)

# Настройка обработки медиафайлов в режиме разработки
if settings.DEBUG:
    # Добавляем обработку медиафайлов
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar
        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass