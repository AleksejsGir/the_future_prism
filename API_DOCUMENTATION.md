# API Documentation - The Future Prism

## Введение

API The Future Prism предоставляет программный доступ к функциональности новостного портала через RESTful интерфейс. Этот документ содержит подробное описание всех доступных эндпоинтов, методов аутентификации и примеров использования API.

**Базовый URL:** `https://api.thefutureprism.com/api/v1/`

## Содержание
1. [Аутентификация](#аутентификация)
2. [Пользователи](#пользователи)
3. [Новости](#новости)
4. [Категории](#категории)
5. [Комментарии](#комментарии)
6. [Избранное](#избранное)
7. [Ошибки и коды состояния](#ошибки-и-коды-состояния)
8. [Пагинация и фильтрация](#пагинация-и-фильтрация)
9. [Ограничение запросов](#ограничение-запросов)
10. [Версионирование](#версионирование)

## Аутентификация

API использует JWT (JSON Web Token) для аутентификации запросов. Для доступа к защищенным эндпоинтам необходимо получить токен и включить его в заголовок запроса.

### Получение токена

```
POST /auth/token/
```

**Тело запроса:**
```json
{
  "username": "user@example.com",
  "password": "your_password"
}
```

**Пример ответа:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Обновление токена

```
POST /auth/token/refresh/
```

**Тело запроса:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Пример ответа:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Использование токена

Для авторизованных запросов добавьте токен в заголовок:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Регистрация нового пользователя

```
POST /auth/register/
```

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "your_password",
  "password_confirm": "your_password"
}
```

## Пользователи

### Получение информации о текущем пользователе

```
GET /users/profile/
```

**Требуется аутентификация:** Да

**Пример ответа:**
```json
{
  "id": 1,
  "username": "username",
  "email": "user@example.com",
  "bio": "Краткая биография пользователя",
  "avatar": "https://api.thefutureprism.com/media/avatars/user_1.jpg",
  "date_joined": "2025-01-15T12:00:00Z",
  "notification_settings": {
    "email_notifications": true,
    "news_updates": true
  }
}
```

### Обновление профиля пользователя

```
PATCH /users/profile/
```

**Требуется аутентификация:** Да

**Тело запроса:**
```json
{
  "bio": "Новая биография пользователя",
  "notification_settings": {
    "email_notifications": false
  }
}
```

### Загрузка аватара

```
POST /users/avatar/
```

**Требуется аутентификация:** Да

**Форма запроса:**
- `avatar`: файл изображения (JPG, PNG, GIF)

**Пример ответа:**
```json
{
  "avatar": "https://api.thefutureprism.com/media/avatars/user_1_new.jpg"
}
```

### Удаление аватара

```
DELETE /users/avatar/
```

**Требуется аутентификация:** Да

## Новости

### Получение списка новостей

```
GET /news/
```

**Параметры запроса:**
- `page`: номер страницы (по умолчанию: 1)
- `page_size`: количество элементов на странице (по умолчанию: 10)
- `category`: идентификатор категории
- `search`: поисковый запрос
- `ordering`: поле для сортировки (например, `-created_at` для сортировки по убыванию даты создания)

**Пример ответа:**
```json
{
  "count": 100,
  "next": "https://api.thefutureprism.com/api/v1/news/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Будущее искусственного интеллекта",
      "slug": "budushchee-iskusstvennogo-intellekta",
      "content": "<p>Полный текст новости...</p>",
      "excerpt": "Краткое описание новости...",
      "image": "https://api.thefutureprism.com/media/news_images/ai_future.jpg",
      "category": {
        "id": 3,
        "name": "Искусственный интеллект",
        "slug": "ai"
      },
      "author": {
        "id": 1,
        "username": "admin",
        "avatar": "https://api.thefutureprism.com/media/avatars/admin.jpg"
      },
      "created_at": "2025-03-10T08:30:00Z",
      "updated_at": "2025-03-10T09:15:00Z",
      "views_count": 1250,
      "comments_count": 45,
      "is_favorite": false
    },
    // Другие новости...
  ]
}
```

### Получение деталей новости

```
GET /news/{id}/
```

**Параметры пути:**
- `id`: идентификатор новости

**Пример ответа:**
```json
{
  "id": 1,
  "title": "Будущее искусственного интеллекта",
  "slug": "budushchee-iskusstvennogo-intellekta",
  "content": "<p>Полный текст новости...</p>",
  "image": "https://api.thefutureprism.com/media/news_images/ai_future.jpg",
  "category": {
    "id": 3,
    "name": "Искусственный интеллект",
    "slug": "ai"
  },
  "author": {
    "id": 1,
    "username": "admin",
    "avatar": "https://api.thefutureprism.com/media/avatars/admin.jpg"
  },
  "created_at": "2025-03-10T08:30:00Z",
  "updated_at": "2025-03-10T09:15:00Z",
  "views_count": 1251,
  "comments_count": 45,
  "is_favorite": true,
  "related_news": [
    {
      "id": 5,
      "title": "Этика в искусственном интеллекте",
      "slug": "etika-v-iskusstvennom-intellekte",
      "excerpt": "Краткое описание...",
      "image": "https://api.thefutureprism.com/media/news_images/ai_ethics.jpg"
    },
    // Другие связанные новости...
  ]
}
```

## Категории

### Получение списка категорий

```
GET /news/categories/
```

**Пример ответа:**
```json
[
  {
    "id": 1,
    "name": "Технологии",
    "slug": "technology",
    "description": "Новости о технологиях",
    "news_count": 42
  },
  {
    "id": 2,
    "name": "Наука",
    "slug": "science",
    "description": "Научные открытия и исследования",
    "news_count": 35
  },
  // Другие категории...
]
```

### Получение новостей по категории

```
GET /news/categories/{slug}/
```

**Параметры пути:**
- `slug`: slug категории

**Параметры запроса:**
- Такие же, как для списка новостей

**Пример ответа:**
```json
{
  "category": {
    "id": 1,
    "name": "Технологии",
    "slug": "technology",
    "description": "Новости о технологиях"
  },
  "news": {
    "count": 42,
    "next": "https://api.thefutureprism.com/api/v1/news/categories/technology/?page=2",
    "previous": null,
    "results": [
      // Новости в категории...
    ]
  }
}
```

## Комментарии

### Получение комментариев к новости

```
GET /news/{news_id}/comments/
```

**Параметры пути:**
- `news_id`: идентификатор новости

**Параметры запроса:**
- `page`: номер страницы
- `page_size`: количество элементов на странице

**Пример ответа:**
```json
{
  "count": 45,
  "next": "https://api.thefutureprism.com/api/v1/news/1/comments/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": {
        "id": 2,
        "username": "user123",
        "avatar": "https://api.thefutureprism.com/media/avatars/user123.jpg"
      },
      "content": "Отличная статья! Очень интересно.",
      "created_at": "2025-03-10T10:15:00Z",
      "updated_at": "2025-03-10T10:15:00Z",
      "parent": null,
      "children": [
        {
          "id": 3,
          "author": {
            "id": 1,
            "username": "admin",
            "avatar": "https://api.thefutureprism.com/media/avatars/admin.jpg"
          },
          "content": "Спасибо за отзыв!",
          "created_at": "2025-03-10T10:30:00Z",
          "updated_at": "2025-03-10T10:30:00Z",
          "parent": 1,
          "children": []
        }
      ]
    },
    // Другие комментарии...
  ]
}
```

### Добавление комментария

```
POST /news/{news_id}/comments/
```

**Требуется аутентификация:** Да

**Параметры пути:**
- `news_id`: идентификатор новости

**Тело запроса:**
```json
{
  "content": "Мой комментарий к новости",
  "parent": null  // Опционально: id родительского комментария для ответа
}
```

**Пример ответа:**
```json
{
  "id": 46,
  "author": {
    "id": 5,
    "username": "current_user",
    "avatar": "https://api.thefutureprism.com/media/avatars/current_user.jpg"
  },
  "content": "Мой комментарий к новости",
  "created_at": "2025-03-14T15:30:00Z",
  "updated_at": "2025-03-14T15:30:00Z",
  "parent": null,
  "children": []
}
```

### Редактирование комментария

```
PATCH /news/{news_id}/comments/{comment_id}/
```

**Требуется аутентификация:** Да

**Параметры пути:**
- `news_id`: идентификатор новости
- `comment_id`: идентификатор комментария

**Тело запроса:**
```json
{
  "content": "Обновленный текст комментария"
}
```

### Удаление комментария

```
DELETE /news/{news_id}/comments/{comment_id}/
```

**Требуется аутентификация:** Да

**Параметры пути:**
- `news_id`: идентификатор новости
- `comment_id`: идентификатор комментария

## Избранное

### Получение списка избранных новостей

```
GET /news/favorites/
```

**Требуется аутентификация:** Да

**Параметры запроса:**
- `page`: номер страницы
- `page_size`: количество элементов на странице

**Пример ответа:**
```json
{
  "count": 12,
  "next": "https://api.thefutureprism.com/api/v1/news/favorites/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Будущее искусственного интеллекта",
      "slug": "budushchee-iskusstvennogo-intellekta",
      "excerpt": "Краткое описание новости...",
      "image": "https://api.thefutureprism.com/media/news_images/ai_future.jpg",
      "category": {
        "id": 3,
        "name": "Искусственный интеллект",
        "slug": "ai"
      },
      "created_at": "2025-03-10T08:30:00Z",
      "added_to_favorites_at": "2025-03-12T14:45:00Z"
    },
    // Другие избранные новости...
  ]
}
```

### Добавление/удаление новости из избранного

```
POST /news/favorites/toggle/{news_id}/
```

**Требуется аутентификация:** Да

**Параметры пути:**
- `news_id`: идентификатор новости

**Пример ответа:**
```json
{
  "status": "added",  // или "removed"
  "news_id": 1,
  "message": "Новость добавлена в избранное"  // или "Новость удалена из избранного"
}
```

## Ошибки и коды состояния

API использует стандартные HTTP-коды состояния для обозначения успеха или неудачи запроса:

* `200 OK`: Запрос выполнен успешно
* `201 Created`: Ресурс успешно создан
* `204 No Content`: Запрос выполнен успешно, но нет содержимого для возврата
* `400 Bad Request`: Некорректный запрос
* `401 Unauthorized`: Отсутствует или недействительный токен аутентификации
* `403 Forbidden`: Доступ к запрашиваемому ресурсу запрещен
* `404 Not Found`: Запрашиваемый ресурс не найден
* `429 Too Many Requests`: Превышено ограничение на количество запросов
* `500 Internal Server Error`: Внутренняя ошибка сервера

В случае ошибки API возвращает JSON-объект с описанием проблемы:

```json
{
  "error": {
    "code": "invalid_credentials",
    "message": "Неверное имя пользователя или пароль",
    "details": {}
  }
}
```

## Пагинация и фильтрация

### Пагинация

API использует пагинацию для возврата больших объемов данных:

**Параметры запроса:**
- `page`: номер страницы (по умолчанию: 1)
- `page_size`: количество элементов на странице (по умолчанию: 10, максимум: 100)

**Пример ответа с пагинацией:**
```json
{
  "count": 100,
  "next": "https://api.thefutureprism.com/api/v1/news/?page=2",
  "previous": null,
  "results": [
    // Элементы...
  ]
}
```

### Фильтрация и сортировка

Многие эндпоинты поддерживают фильтрацию и сортировку:

**Новости:**
- `search`: поиск по ключевым словам
- `category`: фильтрация по категории
- `author`: фильтрация по автору
- `created_after`: новости, созданные после указанной даты (формат: YYYY-MM-DD)
- `created_before`: новости, созданные до указанной даты
- `ordering`: поле для сортировки (например, `-created_at`, `title`)

**Пример запроса с фильтрацией:**
```
GET /news/?search=искусственный+интеллект&category=3&ordering=-created_at
```

## Ограничение запросов

Для защиты от злоупотреблений API применяет ограничения на количество запросов:

- Для анонимных пользователей: 100 запросов в час
- Для аутентифицированных пользователей: 1000 запросов в час

При превышении лимита API возвращает код состояния `429 Too Many Requests`.

**Заголовки ответа API включают информацию о лимитах:**
- `X-RateLimit-Limit`: общий лимит запросов
- `X-RateLimit-Remaining`: оставшееся количество запросов
- `X-RateLimit-Reset`: время в секундах до сброса лимита

## Версионирование

API использует версионирование в URL. Текущая версия: `v1`.

```
https://api.thefutureprism.com/api/v1/
```

При существенных изменениях в API будет выпущена новая версия, например, `v2`. Старые версии будут поддерживаться в течение разумного периода времени для обеспечения обратной совместимости.

## Примеры использования API

### Аутентификация и получение профиля пользователя

```python
import requests

# Аутентификация
auth_response = requests.post(
    "https://api.thefutureprism.com/api/v1/auth/token/",
    json={"username": "user@example.com", "password": "your_password"}
)
token = auth_response.json()["access"]

# Получение профиля
headers = {"Authorization": f"Bearer {token}"}
profile_response = requests.get(
    "https://api.thefutureprism.com/api/v1/users/profile/",
    headers=headers
)
profile = profile_response.json()
```

### Получение списка новостей с фильтрацией

```javascript
// JavaScript (fetch API)
async function getNewsByCategory(categoryId, page = 1) {
    const response = await fetch(
        `https://api.thefutureprism.com/api/v1/news/?category=${categoryId}&page=${page}`,
        { method: 'GET' }
    );
    return await response.json();
}

// Использование
getNewsByCategory(3).then(news => {
    console.log(`Найдено ${news.count} новостей`);
    news.results.forEach(item => {
        console.log(`${item.title} - ${item.created_at}`);
    });
});
```

### Добавление новости в избранное

```python
import requests

# Аутентификация (получение токена)
auth_response = requests.post(
    "https://api.thefutureprism.com/api/v1/auth/token/",
    json={"username": "user@example.com", "password": "your_password"}
)
token = auth_response.json()["access"]

# Добавление новости в избранное
headers = {"Authorization": f"Bearer {token}"}
news_id = 42
favorite_response = requests.post(
    f"https://api.thefutureprism.com/api/v1/news/favorites/toggle/{news_id}/",
    headers=headers
)

# Вывод результата
result = favorite_response.json()
print(result["message"])  # "Новость добавлена в избранное" или "Новость удалена из избранного"
```

## Заключение

API The Future Prism предоставляет гибкие возможности для интеграции с новостным порталом. Для получения дополнительной информации или поддержки, пожалуйста, обращайтесь к команде разработчиков по адресу api@thefutureprism.com.

---

© 2025 The Future Prism. Все права защищены.
