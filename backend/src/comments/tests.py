from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from posts.models import Post
from comments.models import Comment


class CreateCommentTestCase(APITestCase):
    """
    Тесты для эндпоинта создания комментария
    """

    def setUp(self):
        """
        Создаем тестового пользователя и пост
        """
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

    def test_create_comment(self):
        """
        Создаем комментарий к посту
        """
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "parent_id": None,
            "text": "Мой первый комментарий",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, "Мой первый комментарий")

    def test_comment_to_comment_of_different_post(self):
        """
        Пытаемся ответить к комментарию другого поста
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
            "parent_id": parent_comment.id,
            "text": "Неправильная связь",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("parent_id", response.data)

    def test_comment_to_nonexistent_parent(self):
        """
        Пытаемся создать комментарий к несуществующему родительскому комментарию
        """
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "parent_id": 9999,  # несуществующий
            "text": "Ошибка",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_with_empty_text(self):
        """
        Пытаемся создать комментарий с пустым текстом
        """
        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "parent_id": None,
            "text": None,  # так же и с пустой строкой с пробелами
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("text", response.data)

    def test_comment_to_nonexistent_post(self):
        """
        Пытаемся создать комментарий к несуществующему посту
        """
        url = reverse("create_comment")
        data = {
            "post_id": 9999,  # несуществующий
            "parent_id": None,
            "text": "Попытка",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deep_nested_comments_same_post(self):
        """
        Создаем комментарии с глубокой вложенностью
        """
        parent = Comment.objects.create(post=self.post, author=self.user, text="1")
        child = Comment.objects.create(
            post=self.post, author=self.user, parent=parent, text="2"
        )
        grandchild = Comment.objects.create(
            post=self.post, author=self.user, parent=child, text="3"
        )

        url = reverse("create_comment")
        data = {
            "post_id": self.post.id,
            "parent_id": grandchild.id,
            "text": "4 уровень",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 4)
