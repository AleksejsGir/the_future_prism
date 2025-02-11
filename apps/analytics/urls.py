# apps/analytics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikeViewSet, AnalyticsViewSet

router = DefaultRouter()
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'aggregated', AnalyticsViewSet, basename='aggregated')

urlpatterns = [
    path('', include(router.urls)),
]
