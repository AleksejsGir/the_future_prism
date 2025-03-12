# apps/comments/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.comments.api.views import CommentViewSet

router = DefaultRouter()
router.register(r'', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]