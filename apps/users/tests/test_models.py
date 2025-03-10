# apps/users/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Тесты для модели CustomUser."""

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    def test_user_creation(self):
        """Тест создания пользователя."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_get_full_name(self):
        """Тест метода get_full_name."""
        # По умолчанию должен вернуть username
        self.assertEqual(self.user.get_full_name(), 'testuser')

        # С установленными first_name и last_name
        self.user.first_name = 'Test'
        self.user.last_name = 'User'
        self.user.save()
        self.assertEqual(self.user.get_full_name(), 'Test User')

    def test_get_avatar_url(self):
        """Тест метода get_avatar_url."""
        # По умолчанию должен вернуть None
        self.assertIsNone(self.user.get_avatar_url())