"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# core/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home, news_list, news_detail, user_login, profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('news/', news_list, name='news_list'),  # маршрут для списка новостей
    path('news/<int:news_id>/', news_detail, name='news_detail'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile, name='profile'),
    path('api/users/', include('apps.users.urls')),
    path('api/news/', include('apps.news.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]
