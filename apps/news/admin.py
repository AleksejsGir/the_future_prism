# apps/news/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, News
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from django.conf import settings

admin.site.site_header = _("The Future Prism Admin")


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Административный интерфейс для модели Category с поддержкой переводов."""
    list_display = ('id', 'name', 'icon_display', 'description', 'news_count', 'translation_status')
    search_fields = ('name', 'description')
    fields = ['name', 'description', 'icon']  # Добавляем поле icon

    # Настройка для кастомных табов
    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'js/admin/custom-tabs.js',
        )
        css = {
            'screen': (
                'css/admin/custom-tabs.css',
            ),
        }

    def icon_display(self, obj):
        """Отображение иконки в списке категорий"""
        return obj.icon if obj.icon else '-'
    icon_display.short_description = 'Иконка'


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

    def translation_status(self, obj):
        """Показывает статус перевода категории как визуальный индикатор."""
        statuses = []
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                continue
            name_field = f"name_{lang_code}"
            desc_field = f"description_{lang_code}"

            # Проверяем наличие названия
            has_name = bool(getattr(obj, name_field))

            if has_name:
                statuses.append(f'<span style="color: green; font-weight: bold;">{lang_code.upper()}</span>')
            else:
                statuses.append(f'<span style="color: red; font-weight: bold;">{lang_code.upper()}</span>')

        return format_html('&nbsp;&nbsp;'.join(statuses))

    translation_status.short_description = _("Статус переводов")

    # Действия для работы с переводами
    actions = ['copy_main_language_to_all']

    def copy_main_language_to_all(self, request, queryset):
        """Копирует содержимое основного языка во все другие языки"""
        for obj in queryset:
            main_lang_name = obj.name
            main_lang_desc = obj.description

            for lang_code, _ in settings.LANGUAGES:
                if lang_code != settings.LANGUAGE_CODE:
                    setattr(obj, f"name_{lang_code}", main_lang_name)
                    if main_lang_desc:
                        setattr(obj, f"description_{lang_code}", main_lang_desc)
            obj.save()

        # Исправляем ошибку здесь - не используем _() напрямую для форматирования
        message = "Основной язык скопирован во все переводы для {} категорий".format(queryset.count())
        self.message_user(request, message)

    copy_main_language_to_all.short_description = _("Копировать основной язык во все переводы")




@admin.register(News)
class NewsAdmin(TranslationAdmin):
    """Административный интерфейс для модели News с поддержкой переводов."""
    list_display = (
        'id', 'title', 'published_date', 'view_count', 'category', 'image_preview', 'status_tag', 'translation_status')
    list_filter = ('published_date', 'category')
    search_fields = ('title', 'content')
    readonly_fields = ('image_preview', 'view_count')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_date']
    date_hierarchy = 'published_date'
    save_on_top = True
    list_per_page = 15
    actions = ['reset_views', 'copy_main_language_to_all']

    # Настройка табов для разных языков
    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'js/admin/custom-tabs.js',
        )
        css = {
            'screen': (
                'css/admin/custom-tabs.css',
            ),
        }

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'slug', 'category', 'published_date'),
            'description': _('Поля "title" имеют переводимые версии для каждого языка')
        }),
        (_('Содержимое'), {
            'fields': ('content', 'short_description'),
            'description': _(
                'Содержимое статьи доступно для перевода на все поддерживаемые языки. Используйте визуальный редактор для форматирования.')
        }),
        (_('Изображение'), {
            'fields': ('image', 'image_preview'),
            'description': _('Загрузите изображение для новости')
        }),
        (_('Статистика'), {
            'fields': ('view_count',),
            'classes': ('collapse',),
            'description': _('Информация о просмотрах новости')
        }),
    )

    # Создаем конфигурацию TinyMCE с учетом языка пользователя
    def get_form(self, request, obj=None, **kwargs):
        # Текущий язык пользователя в админке
        user_language = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        tinymce_language = 'ru' if user_language in ['ru', 'ru-ru'] else 'en'

        # Оптимизированные настройки TinyMCE
        self.formfield_overrides = {
            models.TextField: {'widget': TinyMCE(
                attrs={'cols': 80, 'rows': 30, 'class': 'custom-tinymce-field'},
                mce_attrs={
                    # Используем только стабильные плагины, убираем устаревшие
                    'plugins': 'advlist autolink lists link image charmap preview hr anchor searchreplace '
                               'visualblocks visualchars code fullscreen table directionality '
                               'emoticons wordcount',
                    'toolbar': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify '
                               '| bullist numlist outdent indent | link image | forecolor backcolor emoticons '
                               '| fullscreen preview code',
                    'style_formats': [
                        {'title': _('Параграф (маленький)'), 'block': 'p', 'classes': 'text-sm'},
                        {'title': _('Параграф (обычный)'), 'block': 'p', 'classes': 'text-base'},
                        {'title': _('Параграф (большой)'), 'block': 'p', 'classes': 'text-lg'},
                        {'title': _('Заголовок 2 (маленький)'), 'block': 'h2', 'classes': 'text-xl'},
                        {'title': _('Заголовок 2 (средний)'), 'block': 'h2', 'classes': 'text-2xl'},
                        {'title': _('Заголовок 2 (большой)'), 'block': 'h2', 'classes': 'text-3xl'},
                        {'title': _('Цвет: Основной'), 'inline': 'span', 'classes': 'text-primary'},
                        {'title': _('Цвет: Дополнительный'), 'inline': 'span', 'classes': 'text-secondary'},
                        {'title': _('Цвет: Акцент'), 'inline': 'span', 'classes': 'text-accent'},
                    ],
                    'body_class': 'custom-tinymce-body',
                    'content_css': [
                        '/static/css/style.css',
                        '/static/css/admin/tinymce-custom.css'
                    ],
                    # Используем язык пользователя
                    'language': tinymce_language,
                    'language_url': f'/static/tinymce/langs/{tinymce_language}.js',
                    'height': 500,
                    'width': '90%',
                    'resize': True,
                    'menubar': 'file edit view insert format tools table help',
                    'contextmenu': 'link image table',
                    'browser_spellcheck': True,
                    'relative_urls': False,
                    'remove_script_host': False,
                    'convert_urls': False,
                    'branding': False,
                    'promotion': False,
                    # Добавляем визуальную индикацию языка редактирования
                    'setup': f"""function(editor) {{
                        editor.on('init', function(e) {{
                            const lang = '{tinymce_language}';
                            const editorContainer = editor.getContainer();

                            // Добавляем индикатор языка в редактор
                            if (editorContainer) {{
                                const flagIndicator = document.createElement('div');
                                flagIndicator.className = 'editor-language-indicator';
                                flagIndicator.innerHTML = lang === 'ru' ? '🇷🇺 Русский' : '🇬🇧 English';
                                flagIndicator.style.position = 'absolute';
                                flagIndicator.style.top = '5px';
                                flagIndicator.style.right = '80px';
                                flagIndicator.style.padding = '3px 8px';
                                flagIndicator.style.borderRadius = '3px';
                                flagIndicator.style.fontSize = '12px';
                                flagIndicator.style.fontWeight = 'bold';
                                flagIndicator.style.backgroundColor = lang === 'ru' ? 'rgba(255,0,0,0.1)' : 'rgba(0,0,255,0.1)';

                                editorContainer.querySelector('.tox-editor-header').appendChild(flagIndicator);
                            }}

                            // Дополнительные настройки после инициализации
                            editor.getBody().style.marginLeft = '0px';
                        }});
                    }}"""
                }
            )}
        }

        return super().get_form(request, obj, **kwargs)

    def image_preview(self, obj):
        """Отображаем превью изображения."""
        if obj.image:
            return format_html('<img src="{}" style="max-width: 150px; max-height:150px;" />', obj.image.url)
        return '-'

    image_preview.short_description = _('Предпросмотр изображения')

    def status_tag(self, obj):
        """Отображаем статус новости на основе количества просмотров."""
        if obj.view_count > 1000:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 4px;">{}</span>',
                _('Популярная')
            )
        elif obj.view_count > 500:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 4px;">{}</span>',
                _('Активная')
            )
        elif obj.view_count > 100:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 4px;">{}</span>',
                _('Обычная')
            )
        else:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 4px;">{}</span>',
                _('Новая')
            )

    status_tag.short_description = _('Статус')

    def translation_status(self, obj):
        """Показывает статус перевода как индикатор на странице списка"""
        statuses = []
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                continue

            # Проверяем наличие заголовка и содержимого
            has_title = bool(getattr(obj, f"title_{lang_code}"))
            has_content = bool(getattr(obj, f"content_{lang_code}"))

            if has_title and has_content:
                statuses.append(f'<span style="color: green; font-weight: bold;">{lang_code.upper()}</span>')
            elif has_title or has_content:
                statuses.append(f'<span style="color: orange; font-weight: bold;">{lang_code.upper()}</span>')
            else:
                statuses.append(f'<span style="color: red; font-weight: bold;">{lang_code.upper()}</span>')

        return format_html('&nbsp;&nbsp;'.join(statuses))

    translation_status.short_description = _("Статус переводов")

    def reset_views(self, request, queryset):
        """Метод для сброса счетчика просмотров."""
        updated = queryset.update(view_count=0)
        # Исправляем ошибку здесь - используем просто строку вместо _().format()
        message = "Счетчик просмотров сброшен для {} новостей.".format(updated)
        self.message_user(request, message)

    reset_views.short_description = _('Сбросить счетчик просмотров')

    def copy_main_language_to_all(self, request, queryset):
        """Копирует содержимое основного языка во все другие языки"""
        updated_count = 0

        for obj in queryset:
            main_title = obj.title
            main_content = obj.content
            main_short_desc = obj.short_description

            for lang_code, _ in settings.LANGUAGES:
                if lang_code != settings.LANGUAGE_CODE:
                    setattr(obj, f"title_{lang_code}", main_title)
                    setattr(obj, f"content_{lang_code}", main_content)
                    if main_short_desc:
                        setattr(obj, f"short_description_{lang_code}", main_short_desc)
            obj.save()
            updated_count += 1

        # Исправляем ошибку здесь - не используем _() для форматирования
        message = "Основной язык скопирован во все переводы для {} новостей".format(updated_count)
        self.message_user(request, message)

    copy_main_language_to_all.short_description = _("Копировать основной язык во все переводы")