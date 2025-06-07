from likes.models import Like
from posts.models import Post
from comments.models import Comment


def get_user_liked_posts(username: str) -> list[Post]:
    """
    Возвращает все лайки, поставленные пользователем с указанным именем к постам.

    Args:
        username: str - имя пользователя

    Returns:
        list[Post]
    """

    likes = Like.objects.filter(
        user__username=username, post__isnull=False
    ).select_related("post__author")

    return [like.post for like in likes]


def get_user_liked_comments(username: str) -> list[Comment]:
    """
    Возвращает все лайки, поставленные пользователем с указанным именем к комментариям.

    Args:
        username: str - имя пользователя

    Returns:
        list[Comment]
    """

    likes = Like.objects.filter(
        user__username=username, comment__isnull=False
    ).select_related("comment__author")

    return [like.comment for like in likes]
