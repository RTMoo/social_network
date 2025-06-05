from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from posts.models import Post
from comments.models import Comment


class CreateCommentTestCase(APITestCase):
    """
    Тесты для эндпоинта создания комментария с полями thread и reply_to
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="romagokz@gmail.com",
            username="testuser",
            password="1234",
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)

        self.post = Post.objects.create(
            author=self.user, title="Test Post", content="Lorem ipsum"
        )

    def test_create_comment_first_level(self):
        """
        Создаем комментарий первого уровня (thread и reply_to должны быть None)
        """
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "thread_id": None,  # thread
            "reply_to_id": None,
            "text": "Мой первый комментарий",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.first()
        self.assertEqual(comment.text, "Мой первый комментарий")
        self.assertIsNone(comment.thread)
        self.assertIsNone(comment.reply_to)

    def test_create_reply_to_comment(self):
        """
        Создаем первый уровень, потом ответ к нему с правильным thread и reply_to
        """
        first_comment = Comment.objects.create(
            post=self.post, author=self.user, text="Первый уровень"
        )

        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "thread_id": first_comment.id,  # thread будет first_comment
            "reply_to_id": first_comment.id,  # reply_to тоже first_comment
            "text": "Ответ на первый уровень",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reply_comment = Comment.objects.get(id=response.data["id"])
        self.assertEqual(reply_comment.thread, first_comment)
        self.assertEqual(reply_comment.reply_to, first_comment)

    def test_create_reply_to_reply(self):
        """
        Создаем ответ к ответу. thread остается тот же, reply_to - конкретный ответ
        """
        first_comment = Comment.objects.create(
            post=self.post, author=self.user, text="Первый уровень"
        )
        reply = Comment.objects.create(
            post=self.post,
            author=self.user,
            thread=first_comment,
            reply_to=first_comment,
            text="Ответ",
        )

        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "thread_id": first_comment.id,  # thread всегда верхний
            "reply_to_id": reply.id,  # отвечаем конкретно на reply
            "text": "Ответ на ответ",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_comment = Comment.objects.get(id=response.data["id"])
        self.assertEqual(new_comment.thread, first_comment)
        self.assertEqual(new_comment.reply_to, reply)

    def test_comment_to_comment_of_different_post(self):
        """
        Пытаемся связать с тредом который нет в текущем посте
        """
        another_post = Post.objects.create(
            author=self.user, title="Another Post", content="Another"
        )

        parent_comment = Comment.objects.create(
            post=self.post, author=self.user, text="Parent comment"
        )

        url = reverse("create_comment")
        data = {
            "post_id": another_post.id,
            "thread_id": parent_comment.id,
            "reply_to_id": parent_comment.id,
            "text": "Неправильная связь",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_to_nonexistent_parent(self):
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "thread_id": 9999,
            "reply_to_id": None,
            "text": "Ошибка",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_with_empty_text(self):
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "thread_id": None,
            "reply_to_id": None,
            "text": None,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("text", response.data)

    def test_comment_to_nonexistent_post(self):
        url = reverse("create_comment")
        data = {
            "post_id": 9999,
            "thread_id": None,
            "reply_to_id": None,
            "text": "Попытка",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
