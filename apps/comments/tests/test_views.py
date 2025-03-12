# apps/comments/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.comments.models import Comment
from apps.news.models import News, Category

User = get_user_model()


class CommentViewsTest(TestCase):
    def setUp(self):
        # Создаем тестового клиента
        self.client = Client()

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

    def test_comment_list_view(self):
        """Тест отображения списка комментариев"""
        url = reverse('comment_list', args=[self.news.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments/comment_list.html')
        self.assertContains(response, 'Test comment content')

    def test_add_comment_unauthorized(self):
        """Тест добавления комментария неавторизованным пользователем"""
        url = reverse('add_comment', args=[self.news.id])
        response = self.client.post(url, {'content': 'New comment'})
        # Должен быть редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_add_comment_authorized(self):
        """Тест добавления комментария авторизованным пользователем"""
        self.client.login(username='testuser', password='password123')
        url = reverse('add_comment', args=[self.news.id])
        response = self.client.post(url, {'content': 'New comment'})
        # Должен быть редирект на страницу новости
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('news_detail', args=[self.news.id]))
        # Проверяем, что комментарий создан
        self.assertTrue(Comment.objects.filter(content='New comment').exists())

    def test_add_reply_to_comment(self):
        """Тест добавления ответа на комментарий"""
        self.client.login(username='testuser', password='password123')
        url = reverse('add_comment', args=[self.news.id])
        response = self.client.post(url, {
            'content': 'Reply to comment',
            'parent_id': self.comment.id
        })
        # Должен быть редирект на страницу новости
        self.assertEqual(response.status_code, 302)
        # Проверяем, что ответ создан
        self.assertTrue(Comment.objects.filter(
            content='Reply to comment',
            parent=self.comment
        ).exists())

    def test_delete_comment_unauthorized(self):
        """Тест удаления комментария неавторизованным пользователем"""
        url = reverse('delete_comment', args=[self.comment.id])
        response = self.client.get(url)
        # Должен быть редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
        # Проверяем, что комментарий не удален
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_authorized(self):
        """Тест удаления комментария авторизованным пользователем"""
        self.client.login(username='testuser', password='password123')
        url = reverse('delete_comment', args=[self.comment.id])
        response = self.client.get(url)
        # Должен быть редирект на страницу новости
        self.assertEqual(response.status_code, 302)
        # Проверяем, что комментарий удален
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_other_user(self):
        """Тест удаления комментария другим пользователем"""
        # Создаем еще одного пользователя
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='password123'
        )
        self.client.login(username='otheruser', password='password123')
        url = reverse('delete_comment', args=[self.comment.id])
        response = self.client.get(url)
        # Должен быть редирект, но комментарий не должен быть удален
        self.assertEqual(response.status_code, 302)
        # Проверяем, что комментарий не удален
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())