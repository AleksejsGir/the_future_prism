"""
Settings for Jazzmin admin panel of The Future Prism project.
"""
# Добавляем импорт для gettext_lazy
from django.utils.translation import gettext_lazy as _

# Jazzmin main settings
JAZZMIN_SETTINGS = {
    # Title on navigation bar
    "site_title": _("The Future Prism"),
    # Title displayed in browser tab
    "site_header": _("The Future Prism Admin"),
    # Title in apps panel
    "site_brand": _("The Future Prism"),
    # Logo link
    "site_logo": "images/logo.PNG",
    # CSS class for logo
    "site_logo_classes": "img-circle",
    # Welcome message on login page
    "welcome_sign": _("Welcome to The Future Prism Admin Panel"),
    # Copyright
    "copyright": _("The Future Prism © 2025"),
    # Custom links displayed on top right
    "topmenu_links": [
        # URL for Home button
        {"name": _("Home"), "url": "admin:index", "permissions": ["auth.view_user"]},
        # External URLs that will open in a new tab
        {"name": _("Go to website"), "url": "/", "new_window": True},
        # User permissions model
        {"model": "auth.User"},
    ],
    # Custom icons for apps/models
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
    # Icons used when custom icons are not defined
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    # Interface theme
    "theme": "darkly",
    # Custom CSS
    "custom_css": "css/themes/admin/admin.css",
    # Custom JS
    "custom_js": None,
    # Hide user models
    "hide_models": [],
    # Sidebar settings
    "order_with_respect_to": ["auth", "users", "news", "comments", "analytics"],
    # Show or hide apps
    "show_ui_builder": True,
    # Make form fields more compact
    "changeform_format": "horizontal",
    # Make form fields more compact
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "collapsible",
    },
}

# Custom UI settings for admin panel
JAZZMIN_UI_TWEAKS = {
    # Оставляем существующие настройки без изменений
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