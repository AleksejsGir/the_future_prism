# apps/comments/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.comments.models import Comment
from apps.news.models import News, Category

User = get_user_model()


class CommentModelTest(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
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
            author=self.user1
        )

        # Создаем родительский комментарий
        self.parent_comment = Comment.objects.create(
            news=self.news,
            author=self.user1,
            content='Parent comment content',
            is_approved=True
        )

        # Создаем дочерний комментарий
        self.child_comment = Comment.objects.create(
            news=self.news,
            author=self.user1,
            content='Child comment content',
            parent=self.parent_comment,
            is_approved=False
        )

    def test_comment_creation(self):
        """Тест создания комментария"""
        self.assertEqual(self.parent_comment.content, 'Parent comment content')
        self.assertTrue(self.parent_comment.is_approved)
        self.assertEqual(self.parent_comment.author, self.user1)
        self.assertEqual(self.parent_comment.news, self.news)
        self.assertIsNone(self.parent_comment.parent)

    def test_comment_parent_child_relationship(self):
        """Тест связи родительский-дочерний комментарий"""
        self.assertEqual(self.child_comment.parent, self.parent_comment)
        self.assertTrue(self.parent_comment.replies.filter(id=self.child_comment.id).exists())

    def test_comment_string_representation(self):
        """Тест строкового представления комментария"""
        self.assertEqual(
            str(self.parent_comment),
            f"Комментарий от {self.user1} к новости '{self.news}'"
        )

    def test_ordering(self):
        """Тест сортировки комментариев"""
        comments = Comment.objects.all()
        self.assertEqual(comments[0], self.parent_comment)
        self.assertEqual(comments[1], self.child_comment)