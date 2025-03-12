# apps/comments/tests/test_api.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.comments.models import Comment
from apps.news.models import News, Category

User = get_user_model()


class CommentAPITest(APITestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

        # Создаем категорию для новости
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Создаем тестовую новость
        self.news = News.objects.create(
            title='Test News',
            content='Test Content',
            category=self.category,
            author=self.user
        )

        # Создаем тестовый комментарий
        self.comment = Comment.objects.create(
            news=self.news,
            author=self.user,
            content='Test comment content',
            is_approved=True
        )

        # URL для API комментариев
        self.url = reverse('comment-list')

    def test_get_comments_list(self):
        """Тест получения списка комментариев через API"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['content'], 'Test comment content')

    def test_create_comment_unauthorized(self):
        """Тест создания комментария неавторизованным пользователем"""
        data = {
            'news': self.news.id,
            'content': 'New API comment'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_authorized(self):
        """Тест создания комментария авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {
            'news': self.news.id,
            'content': 'New API comment'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'New API comment')
        self.assertTrue(Comment.objects.filter(content='New API comment').exists())

    def test_create_reply_to_comment(self):
        """Тест создания ответа на комментарий через API"""
        self.client.force_authenticate(user=self.user)
        data = {
            'news': self.news.id,
            'content': 'Reply via API',
            'parent': self.comment.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Reply via API')
        self.assertEqual(response.data['parent'], self.comment.id)
        self.assertTrue(Comment.objects.filter(
            content='Reply via API',
            parent=self.comment
        ).exists())

    def test_update_comment(self):
        """Тест обновления комментария через API"""
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        data = {
            'news': self.news.id,
            'content': 'Updated comment content'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated comment content')
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content')

    def test_delete_comment(self):
        """Тест удаления комментария через API"""
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())