from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, News
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "The Future Prism Admin"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Category."""
    list_display = ('id', 'name', 'description', 'news_count')
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        """Оптимизируем запрос с аннотацией для подсчета новостей."""
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _news_count=Count('news', distinct=True),
        )
        return queryset

    def news_count(self, obj):
        """Отображаем количество новостей в каждой категории."""
        return obj._news_count

    news_count.short_description = _('Количество новостей')
    news_count.admin_order_field = '_news_count'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели News."""
    list_display = ('id', 'title', 'published_date', 'view_count', 'category', 'image_preview', 'status_tag')
    # Исправляем фильтры - убираем EmptyFieldListFilter для view_count
    list_filter = ('published_date', 'category')
    search_fields = ('title', 'content')
    readonly_fields = ('image_preview', 'view_count')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_date']
    date_hierarchy = 'published_date'
    save_on_top = True
    list_per_page = 20
    actions = ['reset_views']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'published_date')
        }),
        ('Содержимое', {
            'fields': ('content',),
            'description': 'Используйте визуальный редактор для форматирования контента'
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview'),
            'description': 'Загрузите изображение для новости'
        }),
        ('Статистика', {
            'fields': ('view_count',),
            'classes': ('collapse',),
            'description': 'Информация о просмотрах новости'
        }),
    )

    # Настройка TinyMCE для полноценного редактирования
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(
            attrs={'cols': 80, 'rows': 30},
            mce_attrs={
                'plugins': 'advlist autolink lists link image charmap print preview hr anchor searchreplace '
                           'visualblocks visualchars code fullscreen insertdatetime media nonbreaking save table '
                           'contextmenu directionality emoticons template paste textcolor wordcount spellchecker',
                'toolbar1': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify '
                            '| bullist numlist outdent indent | link image media | forecolor backcolor emoticons '
                            '| fullscreen preview code',
                'style_formats': [
                    {'title': 'Параграф', 'block': 'p'},
                    {'title': 'Заголовок 2', 'block': 'h2'},
                    {'title': 'Заголовок 3', 'block': 'h3'},
                    {'title': 'Заголовок 4', 'block': 'h4'},
                    {'title': 'Цитата', 'block': 'blockquote'},
                    {'title': 'Выделенный блок', 'block': 'div', 'classes': 'highlighted-block'},
                ],
                'content_css': '/static/css/style.css',
                'language': 'ru',
                'language_url': '/static/tinymce/langs/ru.js',
                'height': 500,
                'menubar': 'file edit view insert format tools table help',
                'contextmenu': 'link image inserttable | cell row column deletetable',
                'image_advtab': True,
                'paste_data_images': True,
            }
        )}
    }

    def image_preview(self, obj):
        """Отображаем превью изображения."""
        if obj.image:
            return format_html('<img src="{}" style="max-width: 150px; max-height:150px;" />', obj.image.url)
        return '-'

    image_preview.short_description = 'Предпросмотр изображения'

    def status_tag(self, obj):
        """Отображаем статус новости на основе количества просмотров."""
        if obj.view_count > 1000:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px;">Популярная</span>')
        elif obj.view_count > 500:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 4px;">Активная</span>')
        elif obj.view_count > 100:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 4px;">Обычная</span>')
        else:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px;">Новая</span>')

    status_tag.short_description = 'Статус'

    def reset_views(self, request, queryset):
        """Метод для сброса счетчика просмотров."""
        updated = queryset.update(view_count=0)
        self.message_user(request, f'Счетчик просмотров сброшен для {updated} новостей.')

    reset_views.short_description = 'Сбросить счетчик просмотров'