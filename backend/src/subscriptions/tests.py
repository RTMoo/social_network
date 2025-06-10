from rest_framework.test import APITestCase
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
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 201)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)

    def test_delete_subscription(self):
        self.client.post(self.url)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 404)
