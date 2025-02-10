# apps/users/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser

class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Testpass123!',
            'password2': 'Testpass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
