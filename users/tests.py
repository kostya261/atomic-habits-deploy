from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password2': 'testpass123',
            'telegram_chat_id': '123456789'
        }

    def test_user_registration_success(self):
        """Успешная регистрация пользователя"""
        response = self.client.post('/api/users/register/', self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Пользователь успешно зарегистрирован', response.data['message'])

        # Проверяем что пользователь создан
        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.telegram_chat_id, '123456789')

    def test_user_registration_password_mismatch(self):
        """Регистрация с несовпадающими паролями"""
        data = self.user_data.copy()
        data['password2'] = 'different'

        response = self.client.post('/api/users/register/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_registration_duplicate_email(self):
        """Регистрация с уже существующим email"""
        # Сначала создаем пользователя
        self.client.post('/api/users/register/', self.user_data)

        # Пытаемся создать еще одного с тем же email
        response = self.client.post('/api/users/register/', self.user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_update_telegram_chat_id(self):
        """Обновление Telegram Chat ID"""
        # Сначала регистрируем пользователя
        self.client.post('/api/users/register/', self.user_data)

        # Получаем токен
        response = self.client.post('/api/token/', {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        })
        token = response.data['access']

        # Обновляем chat_id
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch('/api/users/telegram/', {
            'telegram_chat_id': '987654321'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['telegram_chat_id'], '987654321')

        # Проверяем в базе
        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(user.telegram_chat_id, '987654321')

    def test_update_telegram_chat_id_unauthorized(self):
        """Попытка обновить chat_id без авторизации"""
        response = self.client.patch('/api/users/telegram/', {
            'telegram_chat_id': '123456'
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTest(TestCase):
    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            email='model@test.com',
            username='modeltest',
            password='test123'
        )

        self.assertEqual(user.email, 'model@test.com')
        self.assertEqual(str(user), 'model@test.com')
        self.assertTrue(user.check_password('test123'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser = User.objects.create_superuser(
            email='admin@test.com',
            username='admin',
            password='admin123'
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_string_representation(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(
            email='string@test.com',
            username='stringtest',
            password='test123'
        )

        self.assertEqual(str(user), 'string@test.com')
