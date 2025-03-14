# API Documentation - The Future Prism

## Introduction

The Future Prism API provides programmatic access to the news portal's functionality through a RESTful interface. This document contains detailed descriptions of all available endpoints, authentication methods, and examples of API usage.

**Base URL:** `https://api.thefutureprism.com/api/v1/`

## Contents
1. [Authentication](#authentication)
2. [Users](#users)
3. [News](#news)
4. [Categories](#categories)
5. [Comments](#comments)
6. [Favorites](#favorites)
7. [Errors and Status Codes](#errors-and-status-codes)
8. [Pagination and Filtering](#pagination-and-filtering)
9. [Rate Limiting](#rate-limiting)
10. [Versioning](#versioning)

## Authentication

The API uses JWT (JSON Web Token) for request authentication. To access protected endpoints, you need to obtain a token and include it in the request header.

### Obtaining a Token

```
POST /auth/token/
```

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "your_password"
}
```

**Example Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Refreshing a Token

```
POST /auth/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Example Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Using the Token

For authenticated requests, add the token to the header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Registering a New User

```
POST /auth/register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "your_password",
  "password_confirm": "your_password"
}
```

## Users

### Get Current User Information

```
GET /users/profile/
```

**Authentication Required:** Yes

**Example Response:**
```json
{
  "id": 1,
  "username": "username",
  "email": "user@example.com",
  "bio": "User's short biography",
  "avatar": "https://api.thefutureprism.com/media/avatars/user_1.jpg",
  "date_joined": "2025-01-15T12:00:00Z",
  "notification_settings": {
    "email_notifications": true,
    "news_updates": true
  }
}
```

### Update User Profile

```
PATCH /users/profile/
```

**Authentication Required:** Yes

**Request Body:**
```json
{
  "bio": "New user biography",
  "notification_settings": {
    "email_notifications": false
  }
}
```

### Upload Avatar

```
POST /users/avatar/
```

**Authentication Required:** Yes

**Request Form:**
- `avatar`: image file (JPG, PNG, GIF)

**Example Response:**
```json
{
  "avatar": "https://api.thefutureprism.com/media/avatars/user_1_new.jpg"
}
```

### Delete Avatar

```
DELETE /users/avatar/
```

**Authentication Required:** Yes

## News

### Get News List

```
GET /news/
```

**Request Parameters:**
- `page`: page number (default: 1)
- `page_size`: number of items per page (default: 10)
- `category`: category ID
- `search`: search query
- `ordering`: field for sorting (e.g., `-created_at` for descending sort by creation date)

**Example Response:**
```json
{
  "count": 100,
  "next": "https://api.thefutureprism.com/api/v1/news/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Future of Artificial Intelligence",
      "slug": "the-future-of-artificial-intelligence",
      "content": "<p>Full news text...</p>",
      "excerpt": "Short news description...",
      "image": "https://api.thefutureprism.com/media/news_images/ai_future.jpg",
      "category": {
        "id": 3,
        "name": "Artificial Intelligence",
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
    // Other news items...
  ]
}
```

### Get News Details

```
GET /news/{id}/
```

**Path Parameters:**
- `id`: news ID

**Example Response:**
```json
{
  "id": 1,
  "title": "The Future of Artificial Intelligence",
  "slug": "the-future-of-artificial-intelligence",
  "content": "<p>Full news text...</p>",
  "image": "https://api.thefutureprism.com/media/news_images/ai_future.jpg",
  "category": {
    "id": 3,
    "name": "Artificial Intelligence",
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
      "title": "Ethics in Artificial Intelligence",
      "slug": "ethics-in-artificial-intelligence",
      "excerpt": "Short description...",
      "image": "https://api.thefutureprism.com/media/news_images/ai_ethics.jpg"
    },
    // Other related news...
  ]
}
```

## Categories

### Get Categories List

```
GET /news/categories/
```

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "News about technology",
    "news_count": 42
  },
  {
    "id": 2,
    "name": "Science",
    "slug": "science",
    "description": "Scientific discoveries and research",
    "news_count": 35
  },
  // Other categories...
]
```

### Get News by Category

```
GET /news/categories/{slug}/
```

**Path Parameters:**
- `slug`: category slug

**Request Parameters:**
- Same as for news list

**Example Response:**
```json
{
  "category": {
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "News about technology"
  },
  "news": {
    "count": 42,
    "next": "https://api.thefutureprism.com/api/v1/news/categories/technology/?page=2",
    "previous": null,
    "results": [
      // News in the category...
    ]
  }
}
```

## Comments

### Get Comments for News

```
GET /news/{news_id}/comments/
```

**Path Parameters:**
- `news_id`: news ID

**Request Parameters:**
- `page`: page number
- `page_size`: number of items per page

**Example Response:**
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
      "content": "Great article! Very interesting.",
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
          "content": "Thank you for your feedback!",
          "created_at": "2025-03-10T10:30:00Z",
          "updated_at": "2025-03-10T10:30:00Z",
          "parent": 1,
          "children": []
        }
      ]
    },
    // Other comments...
  ]
}
```

### Add a Comment

```
POST /news/{news_id}/comments/
```

**Authentication Required:** Yes

**Path Parameters:**
- `news_id`: news ID

**Request Body:**
```json
{
  "content": "My comment on the news",
  "parent": null  // Optional: parent comment ID for replies
}
```

**Example Response:**
```json
{
  "id": 46,
  "author": {
    "id": 5,
    "username": "current_user",
    "avatar": "https://api.thefutureprism.com/media/avatars/current_user.jpg"
  },
  "content": "My comment on the news",
  "created_at": "2025-03-14T15:30:00Z",
  "updated_at": "2025-03-14T15:30:00Z",
  "parent": null,
  "children": []
}
```

### Edit a Comment

```
PATCH /news/{news_id}/comments/{comment_id}/
```

**Authentication Required:** Yes

**Path Parameters:**
- `news_id`: news ID
- `comment_id`: comment ID

**Request Body:**
```json
{
  "content": "Updated comment text"
}
```

### Delete a Comment

```
DELETE /news/{news_id}/comments/{comment_id}/
```

**Authentication Required:** Yes

**Path Parameters:**
- `news_id`: news ID
- `comment_id`: comment ID

## Favorites

### Get Favorite News List

```
GET /news/favorites/
```

**Authentication Required:** Yes

**Request Parameters:**
- `page`: page number
- `page_size`: number of items per page

**Example Response:**
```json
{
  "count": 12,
  "next": "https://api.thefutureprism.com/api/v1/news/favorites/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Future of Artificial Intelligence",
      "slug": "the-future-of-artificial-intelligence",
      "excerpt": "Short news description...",
      "image": "https://api.thefutureprism.com/media/news_images/ai_future.jpg",
      "category": {
        "id": 3,
        "name": "Artificial Intelligence",
        "slug": "ai"
      },
      "created_at": "2025-03-10T08:30:00Z",
      "added_to_favorites_at": "2025-03-12T14:45:00Z"
    },
    // Other favorite news...
  ]
}
```

### Add/Remove News from Favorites

```
POST /news/favorites/toggle/{news_id}/
```

**Authentication Required:** Yes

**Path Parameters:**
- `news_id`: news ID

**Example Response:**
```json
{
  "status": "added",  // or "removed"
  "news_id": 1,
  "message": "News added to favorites"  // or "News removed from favorites"
}
```

## Errors and Status Codes

The API uses standard HTTP status codes to indicate success or failure of a request:

* `200 OK`: Request successful
* `201 Created`: Resource successfully created
* `204 No Content`: Request successful, but no content to return
* `400 Bad Request`: Invalid request
* `401 Unauthorized`: Missing or invalid authentication token
* `403 Forbidden`: Access to the requested resource is forbidden
* `404 Not Found`: The requested resource was not found
* `429 Too Many Requests`: Rate limit exceeded
* `500 Internal Server Error`: Server error

In case of an error, the API returns a JSON object with a description of the problem:

```json
{
  "error": {
    "code": "invalid_credentials",
    "message": "Invalid username or password",
    "details": {}
  }
}
```

## Pagination and Filtering

### Pagination

The API uses pagination for returning large data sets:

**Request Parameters:**
- `page`: page number (default: 1)
- `page_size`: number of items per page (default: 10, maximum: 100)

**Example Paginated Response:**
```json
{
  "count": 100,
  "next": "https://api.thefutureprism.com/api/v1/news/?page=2",
  "previous": null,
  "results": [
    // Items...
  ]
}
```

### Filtering and Sorting

Many endpoints support filtering and sorting:

**News:**
- `search`: search by keywords
- `category`: filter by category
- `author`: filter by author
- `created_after`: news created after specified date (format: YYYY-MM-DD)
- `created_before`: news created before specified date
- `ordering`: field for sorting (e.g., `-created_at`, `title`)

**Example Request with Filtering:**
```
GET /news/?search=artificial+intelligence&category=3&ordering=-created_at
```

## Rate Limiting

To protect against abuse, the API applies request rate limits:

- For anonymous users: 100 requests per hour
- For authenticated users: 1000 requests per hour

When the limit is exceeded, the API returns a `429 Too Many Requests` status code.

**API Response Headers Include Rate Limit Information:**
- `X-RateLimit-Limit`: total request limit
- `X-RateLimit-Remaining`: remaining number of requests
- `X-RateLimit-Reset`: time in seconds until the limit resets

## Versioning

The API uses versioning in the URL. Current version: `v1`.

```
https://api.thefutureprism.com/api/v1/
```

When significant changes are made to the API, a new version will be released, for example, `v2`. Old versions will be supported for a reasonable period of time to ensure backward compatibility.

## API Usage Examples

### Authentication and Retrieving User Profile

```python
import requests

# Authentication
auth_response = requests.post(
    "https://api.thefutureprism.com/api/v1/auth/token/",
    json={"username": "user@example.com", "password": "your_password"}
)
token = auth_response.json()["access"]

# Get profile
headers = {"Authorization": f"Bearer {token}"}
profile_response = requests.get(
    "https://api.thefutureprism.com/api/v1/users/profile/",
    headers=headers
)
profile = profile_response.json()
```

### Getting News List with Filtering

```javascript
// JavaScript (fetch API)
async function getNewsByCategory(categoryId, page = 1) {
    const response = await fetch(
        `https://api.thefutureprism.com/api/v1/news/?category=${categoryId}&page=${page}`,
        { method: 'GET' }
    );
    return await response.json();
}

// Usage
getNewsByCategory(3).then(news => {
    console.log(`Found ${news.count} news items`);
    news.results.forEach(item => {
        console.log(`${item.title} - ${item.created_at}`);
    });
});
```

### Adding News to Favorites

```python
import requests

# Authentication (get token)
auth_response = requests.post(
    "https://api.thefutureprism.com/api/v1/auth/token/",
    json={"username": "user@example.com", "password": "your_password"}
)
token = auth_response.json()["access"]

# Add news to favorites
headers = {"Authorization": f"Bearer {token}"}
news_id = 42
favorite_response = requests.post(
    f"https://api.thefutureprism.com/api/v1/news/favorites/toggle/{news_id}/",
    headers=headers
)

# Output result
result = favorite_response.json()
print(result["message"])  # "News added to favorites" or "News removed from favorites"
```

## Conclusion

The Future Prism API provides flexible capabilities for integration with the news portal. For additional information or support, please contact the development team at api@thefutureprism.com.

---

© 2025 The Future Prism. All rights reserved.
