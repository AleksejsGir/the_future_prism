# apps/news/tests/test_models.py
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from ..models import Category, News

User = get_user_model()


class CategoryModelTest(TestCase):
    """Тесты для модели Category."""

    def setUp(self):
        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            icon="🔥"
        )

    def test_category_creation(self):
        """Тест создания категории."""
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "Test Description")
        self.assertEqual(self.category.icon, "🔥")

    def test_str_representation(self):
        """Тест строкового представления категории."""
        self.assertEqual(str(self.category), "Test Category")


class NewsModelTest(TestCase):
    """Тесты для модели News."""

    def setUp(self):
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
            category=self.category,
            published_date=timezone.now()
        )

    def test_news_creation(self):
        """Тест создания новости."""
        self.assertEqual(self.news.title, "Test News")
        self.assertEqual(self.news.content, "Test Content")
        self.assertEqual(self.news.short_description, "Test Short Description")
        self.assertEqual(self.news.category, self.category)
        self.assertEqual(self.news.view_count, 0)  # Начальное значение

    def test_slug_generation(self):
        """Тест автоматической генерации слага."""
        expected_slug = slugify("Test News")
        self.assertEqual(self.news.slug, expected_slug)

    def test_str_representation(self):
        """Тест строкового представления новости."""
        self.assertEqual(str(self.news), "Test News")

    def test_favorites(self):
        """Тест добавления новости в избранное."""
        # Создаем тестового пользователя
        user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Проверяем, что новость изначально не в избранном
        self.assertFalse(self.news in user.favorites.all())

        # Добавляем новость в избранное
        user.favorites.add(self.news)

        # Проверяем, что новость в избранном
        self.assertTrue(self.news in user.favorites.all())

        # Удаляем новость из избранного
        user.favorites.remove(self.news)

        # Проверяем, что новость удалена из избранного
        self.assertFalse(self.news in user.favorites.all())