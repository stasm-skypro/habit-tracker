from datetime import time, timedelta

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from habit.models import Habit
from user.models import User


class HabitViewSetTestCase(TestCase):
    """
    Класс для тестирования представления HabitViewSet.
    """

    def setUp(self):
        """
        Настраивает тестовые данные.
        :return:
        """
        self.user = User.objects.create_user(
            email="testuser@example.com", first_name="Test", last_name="User", password="pass1234"
        )
        self.other_user = User.objects.create_user(
            email="otheruser@example.com", first_name="Other", last_name="User", password="pass1234"
        )
        self.client: APIClient = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time=time(8, 0),
            action="Do yoga",
            is_pleasant=False,
            periodicity=1,
            duration=timedelta(minutes=30),
            reward="Coffee",
            is_public=False,
        )

        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place="Park",
            time=time(7, 30),
            action="Jogging",
            is_pleasant=True,
            periodicity=1,
            duration=timedelta(minutes=20),
            reward=None,
            is_public=True,
        )

    # Везде, где вызывается .data, добавляем аннотацию: Response, чтобы mypy понимал, что
    # response — это rest_framework.response.Response
    def test_list_user_habits(self):
        """
        Тестирует получение списка пользовательских привычек.
        :return:
        """
        url = reverse("habit:habit-list")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["id"], self.habit.id)

    def test_create_habit(self):
        """
        Тестирует создание привычки.
        :return:
        """
        url = reverse("habit:habit-list")
        data = {
            "place": "Gym",
            "time": "06:30:00",
            "action": "Workout",
            "periodicity": 2,
            "duration": "00:02:00",
            "reward": "Smoothie",
            "is_public": True,
        }
        response: Response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.filter(action="Workout", user=self.user).exists())

    def test_retrieve_habit(self):
        """
        Тестирует получение конкретной привычки.
        :return:
        """
        url = reverse("habit:habit-detail", args=[self.habit.id])
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.habit.id)

    def test_update_habit(self):
        """
        Тестирует обновление привычки.
        :return:
        """
        url = reverse("habit:habit-detail", args=[self.habit.id])
        data = {
            "place": "Office",
            "time": "09:00:00",
            "action": "Meditation",
            "periodicity": 1,
            "duration": "00:01:00",
            "reward": "Tea",
            "is_public": False,
        }
        response: Response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Meditation")

    def test_partial_update_habit(self):
        """
        Тестирует частичное обновление привычки.
        :return:
        """
        url = reverse("habit:habit-detail", args=[self.habit.id])
        response: Response = self.client.patch(url, {"action": "Read book"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Read book")

    def test_delete_habit(self):
        """
        Тестирует удаление привычки.
        :return:
        """
        url = reverse("habit:habit-detail", args=[self.habit.id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_user_cannot_access_others_habit(self):
        """
        Тестирует, что пользователь не может получить доступ к привычке другого пользователя.
        :return:
        """
        other_habit = Habit.objects.create(
            user=self.other_user,
            place="Cafe",
            time=time(10, 0),
            action="Write journal",
            periodicity=1,
            duration=timedelta(minutes=15),
        )
        url = reverse("habit:habit-detail", args=[other_habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habit_list(self):
        """
        Тестирует получение списка публичных привычек.
        :return:
        """
        url = reverse("habit:habit-public")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(h["id"] == self.public_habit.id for h in response.data["results"]))
