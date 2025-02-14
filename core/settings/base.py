import os
from pathlib import Path

# Определяем базовую директорию проекта:
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Секретный ключ (рекомендуется использовать переменную окружения)
SECRET_KEY = os.getenv('SECRET_KEY', 'replace-this-with-a-secure-key')

# По умолчанию DEBUG выключён (будет переопределён в dev.py)
DEBUG = False

ALLOWED_HOSTS = []

# Устанавливаем список приложений Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
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
