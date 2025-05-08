from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class UserTests(APITestCase):
    """
    Класс для тестирования пользователей.
    """

    def setUp(self):
        """
        Настраивает тестовые данные.
        :return:
        """
        self.registration_url = reverse("user:register")
        self.login_url = reverse("user:login")
        self.user_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "StrongPassword123",
        }

    def test_user_registration(self):
        """
        Тестирует регистрацию пользователя.
        :return:
        """
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_user_login_with_valid_credentials(self):
        """
        Тестирует авторизацию пользователя.
        :return:
        """
        User.objects.create_user(
            email=self.user_data["email"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
            password=self.user_data["password"],  # Менеджер сам вызывает set_password()
        )
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_with_invalid_credentials(self):
        """
        Тестирует авторизацию пользователя с неправильными данными.
        :return:
        """
        User.objects.create_user(
            email=self.user_data["email"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
            password=self.user_data["password"],  # Менеджер сам вызывает set_password()
        )
        login_data = {
            "email": self.user_data["email"],
            "password": "WrongPassword",
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_str_representation(self):
        """
        Тестирует строковое представление пользователя.
        :return:
        """
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data["email"])
