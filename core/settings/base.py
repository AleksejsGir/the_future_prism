import os
from pathlib import Path
from .jazzmin_settings import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS

# Определяем базовую директорию проекта:
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Секретный ключ (рекомендуется использовать переменную окружения)
SECRET_KEY = os.getenv('SECRET_KEY', 'replace-this-with-a-secure-key')

# По умолчанию DEBUG выключён (будет переопределён в dev.py)
DEBUG = False

ALLOWED_HOSTS = []

# Устанавливаем список приложений Django
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'tinymce',
    'apps.users',
    'apps.news',  # наше новое приложение
    'apps.comments',  # наше новое приложение для комментариев
    'apps.analytics',  # наше новое приложение для аналитики
]

# Здесь мы указываем Django использовать кастомную модель пользователя.
AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Каталог для шаблонов
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Настройки базы данных будут заданы в dev.py и prod.py

# Настройки статики:
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Дефолтное значение для первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки медиафайлов
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки для загрузки файлов
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Максимальный размер загружаемого файла (5MB)
MAX_UPLOAD_SIZE = 5 * 1024 * 1024

# Разрешенные форматы изображений
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
]

# Максимальные размеры изображения
MAX_IMAGE_DIMENSIONS = {
    'width': 1920,
    'height': 1080,
}

# Размеры для аватара
AVATAR_DIMENSIONS = {
    'width': 300,
    'height': 300,
}
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Настройки TinyMCE - добавить в конец файла
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'width': '100%',
    'height': 500,
    'menubar': 'file edit view insert format tools table help',
    'plugins': 'advlist autolink lists link image charmap print preview hr anchor '
               'searchreplace visualblocks visualchars code fullscreen insertdatetime media '
               'nonbreaking save table contextmenu directionality emoticons template paste '
               'textcolor wordcount spellchecker',
    'toolbar': 'undo redo | formatselect | bold italic backcolor | '
               'alignleft aligncenter alignright alignjustify | '
               'bullist numlist outdent indent | link image media | removeformat | help',
    'language': 'ru',
    'directionality': 'ltr',
    'branding': False,
    'statusbar': True,
    'resize': 'both',
    'elementpath': False,
    'convert_urls': False,
    'valid_elements': '*[*]',
    'extended_valid_elements': 'img[class=responsive|src|border=0|alt|title|width|height|align]',
    'content_css': [
        '/static/css/style.css',
    ],
}

# Используем локальную версию TinyMCE вместо CDN
TINYMCE_JS_URL = '/static/tinymce/tinymce.min.js'
TINYMCE_COMPRESSOR = False