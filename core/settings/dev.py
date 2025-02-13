import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Настройка базы данных PostgreSQL для разработки.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME',),
        'USER': os.getenv('DATABASE_USER',),
        'PASSWORD': os.getenv('DATABASE_PASSWORD',),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# Дополнительные настройки для разработки можно добавить здесь
