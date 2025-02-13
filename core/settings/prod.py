import os
from .base import *

DEBUG = False

# ALLOWED_HOSTS можно задать через переменную окружения
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# Настройка базы данных PostgreSQL для продакшена.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME',),
        'USER': os.getenv('DATABASE_USER',),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# Дополнительные настройки безопасности и продакшен-конфигурация можно добавить здесь.
