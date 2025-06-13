from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser
from friendships.models import FriendshipRequest, Friendship
from rest_framework import status


class FriendshipTests(APITestCase):
    def setUp(self):
        """Создание двух пользователей и функций для получения URL-ов"""
        self.user_1 = CustomUser.objects.create_user(
            email="a@b.com", username="user1", password="pass1234"
        )
        self.user_2 = CustomUser.objects.create_user(
            email="b@c.com", username="user2", password="pass1234"
        )

        self.send_request_url = lambda username: reverse("send_friendship_request", kwargs={"username": username})
        self.reject_request_url = lambda username: reverse("reject_friendship_request", kwargs={"username": username})
        self.accept_friendship_url = lambda username: reverse("accept_friendship_request", kwargs={"username": username})

    def test_send_friendship_request(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(self.send_request_url(self.user_2.username))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FriendshipRequest.objects.count(), 1)

        request = FriendshipRequest.objects.first()
        self.assertEqual(request.from_user, self.user_1)
        self.assertEqual(request.to_user, self.user_2)

    def test_accept_request(self):
        self.client.force_authenticate(user=self.user_1)
        self.client.post(self.send_request_url(self.user_2.username))

        self.client.force_authenticate(user=self.user_2)
        response = self.client.post(self.accept_friendship_url(self.user_1.username))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Friendship.objects.count(), 1)

        friendship = Friendship.objects.first()
        self.assertIn(self.user_1, [friendship.user1, friendship.user2])
        self.assertIn(self.user_2, [friendship.user1, friendship.user2])

    def test_duplicate_request_and_friendship(self):
        self.client.force_authenticate(user=self.user_1)
        response_1 = self.client.post(self.send_request_url(self.user_2.username))
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        response_2 = self.client.post(self.send_request_url(self.user_2.username))
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FriendshipRequest.objects.count(), 1)

        self.client.force_authenticate(user=self.user_2)
        response_3 = self.client.post(self.accept_friendship_url(self.user_1.username))
        self.assertEqual(response_3.status_code, status.HTTP_201_CREATED)

        response_4 = self.client.post(self.accept_friendship_url(self.user_1.username))
        self.assertEqual(response_4.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Friendship.objects.count(), 1)

    def test_reject_request(self):
        self.client.force_authenticate(user=self.user_2)
        self.client.post(self.send_request_url(self.user_1.username))

        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(self.reject_request_url(self.user_2.username))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FriendshipRequest.objects.count(), 0)

        self.client.force_authenticate(user=self.user_2)
        response = self.client.post(self.reject_request_url(self.user_1.username))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=self.user_1)
        response = self.client.post(self.reject_request_url(self.user_2.username))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
