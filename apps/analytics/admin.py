# apps/analytics/admin.py
from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'user', 'created_at')
    list_filter = ('created_at',)
