from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'email': 'testuser@mail.com',
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.is_email_verified = True
        self.user.save()

    def test_register_user(self):
        """Тестирует регистрацию нового пользователя."""
        data = {
            'email': 'newuser@mail.com',
            'username': 'newuser',
            'password': 'newpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['message'],
            'Registration successful. Please check your email to confirm your account.'
        )

    def test_login_user(self):
        """Тестирует вход пользователя с проверенной электронной почтой."""
        data = {
            'email': 'testuser@mail.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_unverified_email(self):
        """Тестирует вход пользователя с
        неподтвержденной электронной почтой."""
        unverified_user = User.objects.create_user(
            email='unverified@mail.com',
            username='unverified',
            password='unverifiedpassword123'
        )
        data = {
            'email': 'unverified@mail.com',
            'password': 'unverifiedpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(
            response.data['non_field_errors'][0], 'Email is not verified.'
        )

    def test_logout_user(self):
        """Тестирует выход пользователя с
        добавлением refresh токена в черный список.
        """
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(
            self.login_url, login_data, format='json'
        )
        refresh_token = login_response.data['refresh']
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        logout_data = {
            'refresh': refresh_token,
            'blacklist': True
        }
        response = self.client.post(
            self.logout_url, logout_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_logout_user_without_blacklist(self):
        """Тестирует выход пользователя без
        добавления refresh токена в черный список."""
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(
            self.login_url, login_data, format='json'
        )
        refresh_token = login_response.data['refresh']
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        logout_data = {
            'refresh': refresh_token,
            'blacklist': False
        }
        response = self.client.post(
            self.logout_url, logout_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')
