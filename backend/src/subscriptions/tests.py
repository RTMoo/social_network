from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from django.urls import reverse


class SubscriptionsTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            username="user",
            password="pass",
        )

        self.other_user = CustomUser.objects.create_user(
            email="other@example.com",
            username="other",
            password="pass",
        )

        self.client.force_authenticate(user=self.user)

        self.url = reverse("subscribe", kwargs={"username": self.other_user.username})

    def test_create_subscription(self):
        """
        Тестирует создание подписки.

        Проверяет:
        - успешное создание подписки (HTTP 201)
        - повторная попытка создать ту же подписку возвращает ошибку (HTTP 400)
        """

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_subscription(self):
        """
        Тестирует удаление подписки.

        Проверяет:
        - успешное удаление существующей подписки (HTTP 204)
        - повторная попытка удалить уже удалённую подписку возвращает ошибку (HTTP 404)
        """

        self.client.post(self.url)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
