# apps/news/admin.py
from django.contrib import admin
from .models import Category, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'published_date', 'view_count')
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'content')
