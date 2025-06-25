from rest_framework.exceptions import NotFound
from posts.models import Post
from subscriptions.selectors import get_user_subscriptions
from likes.models import Like
from accounts.models import CustomUser
from django.db.models import QuerySet


def get_user_posts(username: str) -> QuerySet:
    """
    Возвращает все посты пользователя.

    Args:
        username (str): username пользователя.

    Returns:
        QuerySet: Посты пользователя.
    """
    posts = (
        Post.objects.filter(author__username=username).select_related("author").all()
    )

    return posts


def get_post(post_id: int) -> Post:
    """
    Возвращает пост по id.

    Args:
        post_id (int): id поста.

    Returns:
        Post: Пост.

    Raises:
        NotFound: Если пост не найден.
    """
    post = Post.objects.filter(id=post_id).first()

    if not post:
        raise NotFound()

    return post


def get_subscription_posts(username: str) -> QuerySet:
    """
    Возвращает посты пользователей, на которых подписан указанный пользователь.

    Args:
        username (str): username пользователя.

    Returns:
        QuerySet: Посты подписок.
    """
    subscriptions = get_user_subscriptions(username=username)

    posts = (
        Post.objects.filter(author__username__in=subscriptions)
        .select_related("author")
        .all()
    )

    return posts


def get_all_posts(user: CustomUser) -> QuerySet:
    """
    Возвращает все посты с отметкой лайков пользователя.

    Args:
        user (CustomUser): Пользователь для отметки лайков.

    Returns:
        QuerySet: Все посты с отметкой лайков.
    """
    posts = Post.objects.select_related("author").all()
    post_ids = [p.id for p in posts]
    liked_ids = set(
        Like.objects.filter(user=user, post_id__in=post_ids).values_list(
            "post_id", flat=True
        )
    )
    for post in posts:
        post.is_liked_by_user = post.id in liked_ids

    return posts
