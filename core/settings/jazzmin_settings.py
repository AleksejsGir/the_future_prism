"""
Настройки Jazzmin для админ-панели проекта The Future Prism.
"""

# Основные настройки Jazzmin
JAZZMIN_SETTINGS = {
    # Заголовок на панели навигации
    "site_title": "The Future Prism",
    # Название, отображаемое на вкладке браузера
    "site_header": "The Future Prism Admin",
    # Название в панели приложений
    "site_brand": "The Future Prism",
    # Ссылка на логотип
    "site_logo": "images/logo.PNG",
    # CSS-класс логотипа
    "site_logo_classes": "img-circle",
    # Приветственное сообщение на странице входа
    "welcome_sign": "Добро пожаловать в админ-панель The Future Prism",
    # Авторские права
    "copyright": "The Future Prism © 2025",
    # Пользовательские ссылки для отображения вверху справа
    "topmenu_links": [
        # URL, который будет указан как кнопка "Домой"
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
        # Внешние URL, которые будут открываться в новой вкладке
        {"name": "Перейти на сайт", "url": "/", "new_window": True},
        # Модель пользовательских разрешений
        {"model": "auth.User"},
    ],
    # Пользовательские иконки для приложений/моделей
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users.customuser": "fas fa-user-astronaut",
        "news.article": "fas fa-newspaper",
        "news.category": "fas fa-tags",
        "comments.comment": "fas fa-comments",
        "analytics.pageview": "fas fa-chart-line",
    },
    # Иконки, используемые когда не определены пользовательские иконки
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    # Тема интерфейса
    "theme": "darkly",
    # Пользовательские CSS
    "custom_css": "css/admin-custom.css",
    # Пользовательский JS
    "custom_js": None,
    # Скрыть модели пользователей
    "hide_models": [],
    # Настройки боковой панели
    "order_with_respect_to": ["auth", "users", "news", "comments", "analytics"],
    # Показывать или скрывать приложения
    "show_ui_builder": True,
    # Делать поля форм более компактными
    "changeform_format": "horizontal",
    # Делать поля форм более компактными
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "collapsible",
    },
}

# Пользовательские настройки UI для админ-панели
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}