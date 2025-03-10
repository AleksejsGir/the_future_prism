# apps/news/tests/test_services.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ..models import Category, News
from ..services import (
    create_or_update_category, create_news, update_news,
    increment_view_count, toggle_favorite
)

User = get_user_model()


class CategoryServicesTest(TestCase):
    """Тесты для сервисных функций, связанных с категориями."""

    def test_create_category(self):
        """Тест создания категории."""
        category = create_or_update_category(
            name="Test Category",
            description="Test Description",
            icon="🔥"
        )

        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test Description")
        self.assertEqual(category.icon, "🔥")

    def test_update_category(self):
        """Тест обновления категории."""
        # Создаем категорию
        category = create_or_update_category(
            name="Initial Name",
            description="Initial Description"
        )

        # Обновляем категорию
        updated_category = create_or_update_category(
            name="Updated Name",
            description="Updated Description",
            icon="🔄",
            category_id=category.id
        )

        # Проверяем, что это тот же объект с обновленными данными
        self.assertEqual(category.id, updated_category.id)
        self.assertEqual(updated_category.name, "Updated Name")
        self.assertEqual(updated_category.description, "Updated Description")
        self.assertEqual(updated_category.icon, "🔄")

    def test_update_nonexistent_category(self):
        """Тест обновления несуществующей категории."""
        with self.assertRaises(ValidationError):
            create_or_update_category(
                name="New Name",
                category_id=9999  # Несуществующий ID
            )


class NewsServicesTest(TestCase):
    """Тесты для сервисных функций, связанных с новостями."""

    def setUp(self):
        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

    def test_create_news(self):
        """Тест создания новости."""
        news = create_news(
            title="Test News",
            content="Test Content",
            category=self.category,
            short_description="Test Short Description"
        )

        self.assertEqual(news.title, "Test News")
        self.assertEqual(news.content, "Test Content")
        self.assertEqual(news.short_description, "Test Short Description")
        self.assertEqual(news.category, self.category)

    def test_update_news(self):
        """Тест обновления новости."""
        # Создаем новость
        news = create_news(
            title="Initial Title",
            content="Initial Content",
            category=self.category
        )

        # Обновляем новость
        updated_news = update_news(
            news.id,
            title="Updated Title",
            content="Updated Content",
            update_slug=True
        )

        # Проверяем обновленные данные
        self.assertEqual(updated_news.title, "Updated Title")
        self.assertEqual(updated_news.content, "Updated Content")

    def test_increment_view_count(self):
        """Тест увеличения счетчика просмотров."""
        # Создаем новость
        news = create_news(
            title="Test News",
            content="Test Content",
            category=self.category
        )

        # Проверяем начальное значение
        self.assertEqual(news.view_count, 0)

        # Увеличиваем счетчик
        new_count = increment_view_count(news.id)

        # Проверяем новое значение
        self.assertEqual(new_count, 1)

        # Проверяем, что значение сохранилось в базе
        news.refresh_from_db()
        self.assertEqual(news.view_count, 1)

    def test_toggle_favorite(self):
        """Тест добавления/удаления из избранного."""
        # Создаем новость
        news = create_news(
            title="Test News",
            content="Test Content",
            category=self.category
        )

        # Проверяем, что новость изначально не в избранном
        self.assertFalse(news in self.user.favorites.all())

        # Добавляем в избранное
        is_favorite, message = toggle_favorite(self.user, news.id)

        # Проверяем результат
        self.assertTrue(is_favorite)
        self.assertEqual(message, "Новость добавлена в избранное")

        # Проверяем, что новость теперь в избранном
        self.assertTrue(news in self.user.favorites.all())

        # Удаляем из избранного
        is_favorite, message = toggle_favorite(self.user, news.id)

        # Проверяем результат
        self.assertFalse(is_favorite)
        self.assertEqual(message, "Новость удалена из избранного")

        # Проверяем, что новость больше не в избранном
        self.assertFalse(news in self.user.favorites.all())