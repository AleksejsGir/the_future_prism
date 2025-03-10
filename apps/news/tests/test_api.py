# apps/news/tests/test_api.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Category, News

User = get_user_model()


class CategoryAPITest(APITestCase):
    """Тесты для API категорий."""

    def setUp(self):
        # Создаем тестового пользователя-админа
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )

        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            icon="🔥"
        )

    def test_get_categories(self):
        """Тест получения списка категорий."""
        url = reverse('api-category-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Category")

    def test_create_category_as_admin(self):
        """Тест создания категории администратором."""
        # Логиним администратора
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('api-category-list')
        data = {
            'name': 'New Category',
            'description': 'New Description',
            'icon': '🆕'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(name='New Category').icon, '🆕')

    def test_create_category_as_anonymous(self):
        """Тест создания категории неавторизованным пользователем."""
        url = reverse('api-category-list')
        data = {
            'name': 'New Category',
            'description': 'New Description'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Category.objects.count(), 1)  # Не создана новая категория


class NewsAPITest(APITestCase):
    """Тесты для API новостей."""

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Создаем тестового пользователя-админа
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )

        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

        # Создаем тестовую новость
        self.news = News.objects.create(
            title="Test News",
            content="Test Content",
            short_description="Test Short Description",
            category=self.category
        )

    def test_get_news_list(self):
        """Тест получения списка новостей."""
        url = reverse('api-news-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test News")

    def test_get_news_detail(self):
        """Тест получения детальной информации о новости."""
        url = reverse('api-news-detail', args=[self.news.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test News")
        self.assertEqual(response.data['content'], "Test Content")

        # Проверяем, что счетчик просмотров увеличился
        self.news.refresh_from_db()
        self.assertEqual(self.news.view_count, 1)

    def test_toggle_favorite(self):
        """Тест добавления/удаления новости из избранного."""
        # Логиним пользователя
        self.client.force_authenticate(user=self.user)

        url = reverse('api-news-toggle-favorite', args=[self.news.id])

        # Добавляем в избранное
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_favorite'])

        # Проверяем, что новость в избранном
        self.user.refresh_from_db()
        self.assertTrue(self.news in self.user.favorites.all())

        # Удаляем из избранного
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_favorite'])

        # Проверяем, что новость больше не в избранном
        self.user.refresh_from_db()
        self.assertFalse(self.news in self.user.favorites.all())

    def test_get_favorites(self):
        """Тест получения списка избранных новостей."""
        # Логиним пользователя
        self.client.force_authenticate(user=self.user)

        # Добавляем новость в избранное
        self.user.favorites.add(self.news)

        url = reverse('api-news-favorites')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test News")