import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Настройка базы данных PostgreSQL для разработки.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', 'future_prism'),
        'USER': os.getenv('DATABASE_USER', 'future_prism_user'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'linda1990'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# Дополнительные настройки для разработки можно добавить здесь
