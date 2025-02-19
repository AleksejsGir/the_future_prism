from django.contrib import admin
from django.utils.html import format_html
from .models import Category, News
from tinymce.widgets import TinyMCE
from django.db import models

admin.site.site_header = "The Future Prism Admin"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description') # ✅ Добавил отображение описания
    search_fields = ('name',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_date', 'view_count', 'category', 'image_preview')
    list_filter = ('published_date', 'category')
    search_fields = ('title', 'content') # ✅ Добавил поиск по содержимому
    readonly_fields = ('image_preview',) # ✅ Добавил поле только для чтения
    prepopulated_fields = {'slug': ('title',)}  # ✅ Автозаполнение slug
    ordering = ['-published_date']  # ✅ Сортировка по умолчанию
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', 'image', 'category', 'published_date') # ✅ Добавил slug
        }),
        ('Дополнительные данные', {
            'fields': ('view_count', 'image_preview'), # ✅ Добавил image_preview
            'classes': ('collapse',)
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 15})},  # ✅ Добавил TinyMCE
    }

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 150px; max-height:150px;" />', obj.image.url)
        return '-' # ✅ Добавил отображение изображения
    image_preview.short_description = 'Изображение'
