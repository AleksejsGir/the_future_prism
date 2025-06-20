# Copyright 2024-2025 Aleksejs Giruckis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from pathlib import Path
from .jazzmin_settings import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS


# Определяем базовую директорию проекта:
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Секретный ключ (используем переменную окружения)
SECRET_KEY = os.getenv('SECRET_KEY', 'replace-this-with-a-secure-key')

# По умолчанию DEBUG выключён (будет переопределён в dev.py)
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Получаем список разрешенных хостов из переменной окружения
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]
DEFAULT_LANGUAGE = 'ru'
LANGUAGE_CODE = 'ru'

# Включаем поддержку переводов
USE_I18N = True

# Настройки modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'  # Язык по умолчанию для создания новых записей
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'ru'  # Язык, с которого копировать значения в пустые поля
MODELTRANSLATION_FALLBACK_LANGUAGES = ('ru', 'en')  # Порядок языков при поиске перевода
MODELTRANSLATION_TRANSLATION_FILES = (  # Путь к файлам с настройками переводов моделей
    'apps.news.translation',
)

# Обновляем INSTALLED_APPS: добавляем modeltranslation в начало списка
INSTALLED_APPS = [
    'modeltranslation',  # Новая строка
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
    'core',
    'apps.users',
    'apps.news',
    'apps.comments',
    'apps.analytics',
]

# Добавляем пути для поиска переводов
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Здесь Я указываю Django использует кастомную модель пользователя.
AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Добавляем middleware локализации
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
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # Добавляем i18n процессор
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Настройки базы данных будут заданы в dev.py и prod.py

# Настройки статики:
STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.getenv('STATIC_ROOT', str(BASE_DIR / 'staticfiles'))
STATICFILES_DIRS = [BASE_DIR / 'static']

# Дефолтное значение для первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки медиафайлов
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', str(BASE_DIR / 'media'))

# Настройки для загрузки файлов
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Максимальный размер загружаемого файла (5MB)
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 5 * 1024 * 1024))

# Разрешенные форматы изображений
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
]

# Максимальные размеры изображения
MAX_IMAGE_DIMENSIONS = {
    'width': int(os.getenv('MAX_IMAGE_WIDTH', 1920)),
    'height': int(os.getenv('MAX_IMAGE_HEIGHT', 1080)),
}

# Размеры для аватара
AVATAR_DIMENSIONS = {
    'width': int(os.getenv('AVATAR_WIDTH', 300)),
    'height': int(os.getenv('AVATAR_HEIGHT', 300)),
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.getenv('API_PAGE_SIZE', 10)),
}

# Настройки TinyMCE
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
        '/static/css/admin/tinymce-custom.css'
    ],
}