from likes.models import Like
from posts.models import Post
from comments.models import Comment
from accounts.models import CustomUser
from typing import List


def get_user_liked_posts(username: str) -> List[Post]:
    """
    Возвращает все посты, которые лайкнул пользователь.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[Post]: Список постов, которые лайкнул пользователь.
    """
    likes = Like.objects.filter(
        user__username=username, post__isnull=False
    ).select_related("post__author")

    return [like.post for like in likes]


def get_user_liked_comments(username: str) -> List[Comment]:
    """
    Возвращает все комментарии, которые лайкнул пользователь.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[Comment]: Список комментариев, которые лайкнул пользователь.
    """
    likes = Like.objects.filter(
        user__username=username, comment__isnull=False
    ).select_related("comment__author")

    return [like.comment for like in likes]


def user_liked_post_exists(user: CustomUser, post: Post) -> bool:
    """
    Возвращает True, если пользователь лайкнул пост.
    """

    return Like.objects.filter(user=user, post=post).exists()
