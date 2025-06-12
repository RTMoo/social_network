from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser
from friendships.models import FriendshipRequest, Friendship
from rest_framework import status


class FriendshipTests(APITestCase):
    def setUp(self):
        """Создание двух пользователей и URL-ов для тестов"""
        self.user_1 = CustomUser.objects.create_user(
            email="a@b.com", username="user1", password="pass1234"
        )
        self.user_2 = CustomUser.objects.create_user(
            email="b@c.com", username="user2", password="pass1234"
        )

        self.request_url = reverse("friendship_request")
        self.friendship_url = reverse("friendship")

    def test_create_friendship_request(self):
        """
        Тестирует успешное создание запроса в друзья
        """
        self.client.force_authenticate(user=self.user_1)
        data = {"to_user": self.user_2.username}
        response = self.client.post(self.request_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FriendshipRequest.objects.count(), 1)

        request = FriendshipRequest.objects.first()
        self.assertEqual(request.from_user, self.user_1)
        self.assertEqual(request.to_user, self.user_2)

    def test_create_friendship(self):
        """
        Тестирует успешное принятие заявки в друзья и создание дружбы
        """
        # user_1 отправляет заявку
        self.client.force_authenticate(user=self.user_1)
        self.client.post(self.request_url, data={"to_user": self.user_2.username})

        # user_2 принимает заявку
        self.client.force_authenticate(user=self.user_2)
        response = self.client.post(
            self.friendship_url, data={"from_user": self.user_1.username}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 1)

        friendship = Friendship.objects.first()
        self.assertIn(self.user_1, [friendship.user1, friendship.user2])
        self.assertIn(self.user_2, [friendship.user1, friendship.user2])

    def test_duplicate_request_and_friendship(self):
        """
        Проверяет поведение при повторном запросе и повторном принятии дружбы
        """
        # user_1 отправляет заявку
        self.client.force_authenticate(user=self.user_1)
        response_1 = self.client.post(
            self.request_url, data={"to_user": self.user_2.username}
        )
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        # Повторный запрос — ошибка
        response_2 = self.client.post(
            self.request_url, data={"to_user": self.user_2.username}
        )
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FriendshipRequest.objects.count(), 1)

        # user_2 принимает заявку
        self.client.force_authenticate(user=self.user_2)
        response_3 = self.client.post(
            self.friendship_url, data={"from_user": self.user_1.username}
        )
        self.assertEqual(response_3.status_code, status.HTTP_201_CREATED)

        # Повторная попытка принять — ошибка (заявка уже удалена)
        response_4 = self.client.post(
            self.friendship_url, data={"from_user": self.user_1.username}
        )
        self.assertEqual(response_4.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Friendship.objects.count(), 1)
