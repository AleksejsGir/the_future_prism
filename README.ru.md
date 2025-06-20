# 🌟 The Future Prism - Новостной портал о технологиях и будущем 🚀

**"The Future Prism"** — это современный новостной портал, посвящённый технологиям, обществу и будущему. Платформа предоставляет удобный интерфейс для чтения, публикации и обсуждения новостей.

---

## 📌 Основные особенности проекта

✅ Интуитивно понятный интерфейс  
✅ Разделение по категориям новостей  
✅ Расширенные профили пользователей с аватарами  
✅ Система комментариев и лайков  
✅ Избранные статьи с персональным списком  
✅ Адаптивный современный дизайн  
✅ Оптимизированная API-интеграция  
✅ Многоязычный интерфейс  

---

## 🏗️ Технологический стек

### 🔹 **Backend**
- **Язык программирования:** Python 3.11  
- **Фреймворк:** Django 5.1  
- **СУБД:** PostgreSQL 13  
- **Кэширование:** Redis 6  
- **Асинхронные задачи:** Celery  
- **Аутентификация:** JWT (DRF SimpleJWT)  
- **REST API:** Django REST Framework  
- **Документация API:** Swagger/OpenAPI (drf-yasg)  

### 🎨 **Frontend**
- **Языки:** HTML5, CSS3, JavaScript  
- **Стилизация:** Tailwind CSS  
- **Редактор контента:** TinyMCE  
- **Интерактивные компоненты:** HTMX  

### ⚙️ **Инфраструктура**
- **Контейнеризация:** Docker + Docker Compose  
- **CI/CD:** GitHub Actions  
- **Веб-сервер:** Gunicorn + Nginx  
- **Логирование и мониторинг**  

---

## 📂 Структура проекта

Проект следует модульной архитектуре с разделением на ядро и независимые приложения:

```
the_future_prism/
├── core/                 # Ядро проекта
│   ├── settings/         # Настройки для разных сред (dev, prod)
│   ├── urls.py           # Основные URL-маршруты
│   └── views.py          # Общие представления
├── apps/                 # Приложения проекта
│   ├── users/            # Пользовательская система
│   │   ├── api/          # API компоненты
│   │   └── services.py   # Бизнес-логика
│   ├── news/             # Модуль публикации новостей
│   │   ├── api/          # API компоненты
│   │   └── services.py   # Бизнес-логика
│   ├── comments/         # Управление комментариями
│   └── analytics/        # Анализ данных и статистика
├── templates/            # Общие шаблоны
│   ├── base.html
│   └── includes/         # Повторно используемые компоненты
├── static/               # Общие статические файлы
└── media/                # Загружаемые пользователем файлы
```

Каждое приложение содержит:
- Свои модели, представления, формы
- Сервисный слой для бизнес-логики
- Отдельные API-компоненты
- Специфические статические файлы
- Тесты для всех компонентов

---

## 🛠️ Установка и запуск

### 🔹 **Предварительные требования**
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker (по желанию)
- Виртуальное окружение Python (рекомендуется)

### 🔹 **Шаги по установке**
1. Клонировать репозиторий:
```bash
git clone https://github.com/AleksejsGir/the_future_prism.git
cd the_future_prism
```

2. Создать виртуальное окружение и установить зависимости:
```bash
python -m venv venv
source venv/bin/activate  # (Linux/macOS) или venv\Scripts\activate  # (Windows)
pip install -r requirements.txt
```

3. Настроить `.env` файл (пример `.env.example`)

4. Применить миграции и запустить сервер:
```bash
python manage.py migrate
python manage.py runserver
```

5. Создать суперпользователя для доступа к админ-панели:
```bash
python manage.py createsuperuser
```

### 🔹 **Запуск через Docker**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🔥 API и интеграции

- **REST API** с полным доступом к функциональности  
- **Swagger/OpenAPI** документация  
- **JWT аутентификация** для безопасного доступа  
- **Фильтрация и поиск** для всех ресурсов  
- **Пагинация и кэширование**  

📌 **API-документация доступна по адресу:**  
`/api/docs/` (Swagger UI)

Подробная документация API находится в файле [API_DOCUMENTATION.ru.md](API_DOCUMENTATION.ru.md)

---

## 🔒 Безопасность и оптимизация

🔹 Защита от XSS, CSRF и SQL-инъекций  
🔹 Ограничение частоты запросов (Rate Limiting)  
🔹 Оптимизация запросов с использованием select_related и prefetch_related  
🔹 Кэширование запросов через Redis  
🔹 Отложенная загрузка изображений  
🔹 Минимизация CSS и JavaScript  

---

## 📊 Тестирование

Проект содержит обширный набор тестов для всех компонентов:

```bash
# Запуск всех тестов
python manage.py test

# Запуск тестов для конкретного приложения
python manage.py test apps.news

# Запуск тестов с отчетом о покрытии
coverage run --source='.' manage.py test
coverage report
```

---

## 🌍 Развертывание

📦 **Docker**  
```bash
docker-compose up --build
```

📡 **Production (Gunicorn + Nginx)**  
```bash
docker-compose -f docker-compose.prod.yml up -d
```

⏳ **CI/CD (GitHub Actions)**  
- Автоматические тесты при каждом push и pull request  
- Безопасное хранение секретов  
- Автоматическое развертывание при merge в main  

Пример CI/CD конфигурации можно найти в файле [.github/workflows/ci.yml](.github/workflows/ci.yml)

---

## 📅 Текущая стадия разработки

### ✅ **Завершено**
✔️ Базовая архитектура и модульная структура  
✔️ Авторизация, профили пользователей с аватарами  
✔️ Основной функционал новостей и категорий  
✔️ Система избранных статей  
✔️ Настроено безопасное развертывание  
✔️ Оптимизация статических файлов  
✔️ Документация API  

### 🔄 **В процессе**
🔸 Улучшение комментариев  
🔸 Добавление аналитики  
🔸 Оптимизация производительности  

### 🚀 **Планируется**
🔹 Интеграция с социальными сетями  
🔹 Расширенный поиск с релевантностью  
🔹 Рекомендательная система на основе предпочтений  
🔹 Разработка мобильного приложения  

---

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта The Future Prism:

1. Сделайте форк репозитория
2. Создайте свою ветку (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте изменения в свой форк (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
See the [NOTICE](NOTICE) file for attribution.

## 👨‍💻 Author

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/AleksejsGir">
          <img src="https://github.com/AleksejsGir.png" width="100px;" alt="Aleksejs Giruckis"/>
          <br />
          <sub><b>Aleksejs Giruckis</b></sub>
        </a>
        <br />
        <sub>Full-Stack Developer</sub>
        <br />
        <a href="https://github.com/AleksejsGir">GitHub</a> •
        <a href="mailto:aleksej.it.gir@gmail.com">Email</a> •
        <a href="https://linkedin.com/in/aleksejs-giruckis-0569a7353">LinkedIn</a>
      </td>
    </tr>
  </table>
</div>

---

## 🎉 Благодарности

Проект разрабатывается с использованием лучших практик Django и современных технологий.

💡 **The Future Prism** — это ваш портал в мир будущего!  
📧 **Контакты:** [aleksej.it.gir@gmail.com](mailto:aleksej.it.gir@gmail.com)

---