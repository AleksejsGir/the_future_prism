# apps/users/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class UserViewsTest(TestCase):
    """Тесты для веб-представлений пользователей."""

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.client = Client()

    def test_login_view(self):
        """Тест страницы входа."""
        # Проверяем GET-запрос
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        # Проверяем POST-запрос с правильными данными
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertRedirects(response, reverse('profile'))

        # Проверяем, что пользователь авторизован
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_profile_view(self):
        """Тест страницы профиля (требует авторизации)."""
        # Без авторизации должен быть редирект
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

        # С авторизацией должен показать профиль
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')