
# The Future Prism 🌟

The Future Prism — это современный новостной портал, построенный на Django с футуристическим дизайном, полной адаптивностью и REST API.

## 🚀 Технологии

### Backend
- Django 5.x
- Django REST Framework (DRF)
- PostgreSQL
- Redis
- Celery

### Frontend
- Tailwind CSS
- DaisyUI
- Минимальный JavaScript

### Инфраструктура
- Docker
- Railway.app
- CI/CD через GitHub Actions

## 🏗 Структура проекта

```
the_future_prism/
├── core/                      # Базовые настройки Django
│   ├── settings/             # Настройки проекта
│   │   ├── base.py          # Общие настройки
│   │   ├── dev.py           # Настройки для разработки
│   │   └── prod.py          # Настройки для продакшена
│   └── urls.py              # Главные маршруты
├── apps/                     # Django-приложения
│   ├── users/               # Пользователи и аутентификация
│   ├── news/                # Новости (CRUD)
│   ├── comments/            # Комментарии
│   └── analytics/           # Аналитика
├── static/                  # Статические файлы
├── templates/               # HTML-шаблоны
└── infra/                   # Инфраструктура проекта
```

## 🎨 Дизайн

- Неоновые акценты
- Градиенты
- Футуристический стиль
- Адаптивный дизайн

### Цветовая палитра
- Electric Blue #4FD6FF
- Neon Pink #FF78FF
- Midnight Gray #2B2B36
- White #F0F0F0

## 🛠 Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/AleksejsGir/the_future_prism.git
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env и настройте переменные окружения

5. Выполните миграции:
```bash
python manage.py migrate
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

## 📊 Основной функционал

- Регистрация и аутентификация пользователей (JWT)
- CRUD операции для новостей
- Древовидные комментарии
- Аналитика (просмотры, лайки)
- REST API
- Модерация контента

## 🔒 Безопасность

- Переменные окружения
- CSRF защита
- Rate limiting для API
- HTTPS (Cloudflare)

## 🚀 Деплой

Проект развернут на Railway.app с использованием CI/CD через GitHub Actions.

## 📝 Лицензия

This project is licensed under the MIT License - see the LICENSE file for details.

