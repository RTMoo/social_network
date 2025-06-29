from typing import List, Set

from rest_framework.exceptions import NotFound
from posts.models import Post
from subscriptions.selectors import get_user_subscription_profiles
from likes.models import Like
from accounts.models import CustomUser
from django.db.models import QuerySet


def get_user_liked_current_post_ids(
    user: CustomUser,
    posts: List[Post],
) -> Set[int]:
    """
    Возвращает множество id постов, которые лайкнул пользователь.

    Args:
        user (CustomUser): Пользователь, для которого нужно получить лайкнутые посты.
        posts (List[Post]): Список постов для проверки.

    Returns:
        Set[int]: Множество id постов, которые лайкнул пользователь.
    """

    post_ids = [post.id for post in posts]
    liked_ids = set(
        Like.objects.filter(user=user, post_id__in=post_ids).values_list(
            "post_id", flat=True
        )
    )

    return liked_ids


def get_user_posts(username: str, sender: CustomUser) -> QuerySet:
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
    liked_ids = get_user_liked_current_post_ids(user=sender, posts=posts)

    for post in posts:
        post.is_liked_by_user = post.id in liked_ids

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
    subscriptions = get_user_subscription_profiles(username=username)

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
    liked_ids = get_user_liked_current_post_ids(user=user, posts=posts)

    for post in posts:
        post.is_liked_by_user = post.id in liked_ids

    return posts
