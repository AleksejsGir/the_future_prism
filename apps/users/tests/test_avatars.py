from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings
import os
import shutil
from PIL import Image
import tempfile

User = get_user_model()


class AvatarTest(TestCase):
    def setUp(self):
        """
        Подготовка окружения для каждого теста.
        Создаём тестового пользователя и временную директорию для медиафайлов.
        """
        # Создаём тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

        # Создаём временную директорию для медиафайлов
        self.temp_media_dir = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self.temp_media_dir

    def tearDown(self):
        """
        Очистка после каждого теста.
        Удаляем временные файлы и директории.
        """
        # Удаляем временную директорию
        shutil.rmtree(self.temp_media_dir, ignore_errors=True)

    def create_test_image(self, filename='test.jpg', size=(100, 100)):
        """
        Создаёт тестовое изображение для загрузки.

        Args:
            filename (str): Имя файла
            size (tuple): Размер изображения (ширина, высота)

        Returns:
            SimpleUploadedFile: Объект файла для загрузки
        """
        image = Image.new('RGB', size, color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(temp_file, format='JPEG')
        temp_file.seek(0)
        return SimpleUploadedFile(filename, temp_file.read(), content_type='image/jpeg')

    def test_avatar_upload(self):
        """Проверяет загрузку аватара через форму редактирования профиля."""
        # Создаём тестовое изображение
        avatar = self.create_test_image()

        # Отправляем POST-запрос на обновление профиля
        response = self.client.post(
            reverse('edit_profile'),
            {'avatar': avatar},
            follow=True
        )

        # Проверяем успешность загрузки
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in [m.tags for m in response.context['messages']])

        # Проверяем, что файл был сохранён
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.avatar)
        self.assertTrue(os.path.exists(user.avatar.path))

    def test_avatar_update(self):
        """Проверяет обновление существующего аватара."""
        # Загружаем первый аватар
        first_avatar = self.create_test_image('first.jpg')
        self.client.post(reverse('edit_profile'), {'avatar': first_avatar})

        # Сохраняем путь к первому аватару
        user = User.objects.get(id=self.user.id)
        first_avatar_path = user.avatar.path

        # Загружаем второй аватар
        second_avatar = self.create_test_image('second.jpg')
        self.client.post(reverse('edit_profile'), {'avatar': second_avatar})

        # Проверяем, что первый файл был удалён
        self.assertFalse(os.path.exists(first_avatar_path))

        # Проверяем, что новый файл существует
        user.refresh_from_db()
        self.assertTrue(os.path.exists(user.avatar.path))

    def test_avatar_delete(self):
        """Проверяет удаление аватара."""
        # Сначала загружаем аватар
        avatar = self.create_test_image()
        self.client.post(reverse('edit_profile'), {'avatar': avatar})

        # Сохраняем путь к файлу
        user = User.objects.get(id=self.user.id)
        avatar_path = user.avatar.path

        # Удаляем аватар
        response = self.client.post(reverse('delete_avatar'), follow=True)

        # Проверяем успешность удаления
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in [m.tags for m in response.context['messages']])

        # Проверяем, что файл был удалён
        user.refresh_from_db()
        self.assertFalse(user.avatar)
        self.assertFalse(os.path.exists(avatar_path))

    def test_avatar_validation(self):
        """Проверяет валидацию загружаемых файлов."""
        # Создаём слишком большое изображение
        large_avatar = self.create_test_image(size=(3000, 3000))

        # Пытаемся загрузить большое изображение
        response = self.client.post(
            reverse('edit_profile'),
            {'avatar': large_avatar},
            follow=True
        )

        # Проверяем наличие ошибки
        self.assertTrue('error' in [m.tags for m in response.context['messages']])

        # Проверяем, что аватар не был сохранён
        user = User.objects.get(id=self.user.id)
        self.assertFalse(user.avatar)

    def test_non_image_upload(self):
        """Проверяет загрузку неверного типа файла."""
        # Создаём текстовый файл
        text_file = SimpleUploadedFile(
            "document.txt",
            b"This is not an image",
            content_type="text/plain"
        )

        # Пытаемся загрузить текстовый файл как аватар
        response = self.client.post(
            reverse('edit_profile'),
            {'avatar': text_file},
            follow=True
        )

        # Проверяем наличие ошибки
        self.assertTrue('error' in [m.tags for m in response.context['messages']])

        # Проверяем, что файл не был сохранён
        user = User.objects.get(id=self.user.id)
        self.assertFalse(user.avatar)