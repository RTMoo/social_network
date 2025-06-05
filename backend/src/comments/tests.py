from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.urls import reverse
from accounts.models import CustomUser
from posts.models import Post
from comments.models import Comment
from comments.services import update_comment


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
            "reply_to_id": first_comment.id,
            "text": "Ответ на первый уровень",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)

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
            "reply_to_id": parent_comment.id,
            "text": "Неправильная связь",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_to_nonexistent_parent(self):
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "reply_to_id": 9999,
            "text": "Ошибка",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_with_empty_text(self):
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
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
            "reply_to_id": None,
            "text": "Попытка",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateCommentTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", username="user", password="pass", is_active=True
        )
        self.other_user = CustomUser.objects.create_user(
            email="other@example.com", username="other", password="pass", is_active=True
        )
        self.client.force_authenticate(user=self.user)

        self.post = Post.objects.create(
            author=self.user, title="Post", content="Content"
        )
        self.another_post = Post.objects.create(
            author=self.user, title="Another", content="Content"
        )

        self.comment = Comment.objects.create(
            post=self.post, author=self.user, text="Original"
        )
        self.reply_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            thread=self.comment,
            reply_to=self.comment,
            text="Reply",
        )

    def test_update_text_success(self):
        data = {"text": "Обновленный текст"}
        updated = update_comment(data, comment_id=self.comment.id, sender=self.user)
        self.assertEqual(updated.text, "Обновленный текст")

    def test_update_reply_to_success(self):
        data = {"reply_to_id": self.comment.id}
        updated = update_comment(
            data, comment_id=self.reply_comment.id, sender=self.user
        )
        self.assertEqual(updated.reply_to, self.comment)

    def test_update_reply_to_invalid_post(self):
        another_comment = Comment.objects.create(
            post=self.another_post, author=self.user, text="Чужой пост"
        )
        data = {"reply_to_id": another_comment.id}
        with self.assertRaises(ValidationError):
            update_comment(data, comment_id=self.comment.id, sender=self.user)

    def test_cannot_update_reply_to_to_none_on_reply(self):
        # reply_comment изначально указывает на comment
        data = {"reply_to_id": None}
        with self.assertRaises(ValidationError):
            update_comment(data, comment_id=self.reply_comment.id, sender=self.user)

    def test_update_by_non_author(self):
        data = {"text": "Не должно получиться"}
        with self.assertRaises(PermissionDenied):
            update_comment(data, comment_id=self.comment.id, sender=self.other_user)
