import os
from .base import *

# Отключаем режим отладки
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS из переменной окружения
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

# Настройка базы данных PostgreSQL для продакшена
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
        'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', 60)),
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# Настройки безопасности для продакшена
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', 31536000))  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() == 'true'
SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD', 'True').lower() == 'true'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').lower() == 'true'

# Настройки кэширования для продакшена
CACHES = {
    'default': {
        'BACKEND': os.getenv(
            'CACHE_BACKEND',
            'django.core.cache.backends.redis.RedisCache'
        ),
        'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/1'),
    }
}

# Настройки электронной почты
EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@thefutureprism.com')

# Настройки логирования для продакшена
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv('LOG_FILE', str(BASE_DIR / 'production.log')),
            'maxBytes': int(os.getenv('LOG_MAX_BYTES', 1024*1024*10)),  # 10MB
            'backupCount': int(os.getenv('LOG_BACKUP_COUNT', 10)),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': True,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': os.getenv('APP_LOG_LEVEL', 'ERROR'),
            'propagate': False,
        },
    },
}

# Настройки статических файлов для продакшена
STATICFILES_STORAGE = os.getenv(
    'STATICFILES_STORAGE',
    'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
)

# Настройки для медиафайлов
MEDIA_ROOT = os.getenv('MEDIA_ROOT', str(BASE_DIR / 'media'))
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')