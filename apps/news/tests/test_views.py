# apps/news/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Category, News
from ..services import create_news

User = get_user_model()


class NewsViewsTest(TestCase):
    """Тесты для представлений новостей."""

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

        # Создаем тестовые новости
        self.news1 = create_news(
            title="Test News 1",
            content="Test Content 1",
            category=self.category
        )

        self.news2 = create_news(
            title="Test News 2",
            content="Test Content 2",
            category=self.category
        )

        # Создаем тестовый клиент
        self.client = Client()

    def test_news_list_view(self):
        """Тест страницы списка новостей."""
        # Проверяем GET-запрос
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')

        # Проверяем контекст
        self.assertIn('news_list', response.context)
        self.assertIn('categories', response.context)

        # Проверяем, что наши тестовые новости в списке
        self.assertIn(self.news1, response.context['news_list'])
        self.assertIn(self.news2, response.context['news_list'])

    def test_news_detail_view(self):
        """Тест страницы детального просмотра новости."""
        # Проверяем GET-запрос
        response = self.client.get(reverse('news_detail', args=[self.news1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')

        # Проверяем контекст
        self.assertEqual(response.context['news'], self.news1)
        self.assertIn('categories', response.context)
        self.assertIn('is_favorite', response.context)
        self.assertIn('similar_news', response.context)

        # Проверяем, что счетчик просмотров увеличился
        self.news1.refresh_from_db()
        self.assertEqual(self.news1.view_count, 1)

    def test_toggle_favorite_view(self):
        """Тест добавления/удаления новости из избранного."""
        # Логиним пользователя
        self.client.login(username="testuser", password="password123")

        # Проверяем, что новость изначально не в избранном
        self.assertFalse(self.news1 in self.user.favorites.all())

        # Добавляем в избранное
        response = self.client.post(reverse('toggle_favorite', args=[self.news1.id]))
        self.assertRedirects(response, reverse('news_detail', args=[self.news1.id]))

        # Проверяем, что новость теперь в избранном
        self.user.refresh_from_db()
        self.assertTrue(self.news1 in self.user.favorites.all())

        # Удаляем из избранного
        response = self.client.post(reverse('toggle_favorite', args=[self.news1.id]))
        self.assertRedirects(response, reverse('news_detail', args=[self.news1.id]))

        # Проверяем, что новость больше не в избранном
        self.user.refresh_from_db()
        self.assertFalse(self.news1 in self.user.favorites.all())

    def test_favorite_news_list_view(self):
        """Тест страницы избранных новостей."""
        # Логиним пользователя
        self.client.login(username="testuser", password="password123")

        # Добавляем новость в избранное
        self.user.favorites.add(self.news1)

        # Проверяем GET-запрос
        response = self.client.get(reverse('favorite_news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/favorites_list.html')

        # Проверяем контекст
        self.assertIn('news_list', response.context)
        self.assertIn('categories', response.context)

        # Проверяем, что наша избранная новость в списке
        self.assertIn(self.news1, response.context['news_list'])

        # Проверяем, что другая новость не в списке
        self.assertNotIn(self.news2, response.context['news_list'])