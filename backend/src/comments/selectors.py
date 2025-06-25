from typing import List, Set
from rest_framework.exceptions import NotFound
from comments.models import Comment
from likes.models import Like
from accounts.models import CustomUser
from django.db.models import QuerySet


def get_user_liked_current_comment_ids(
    user: CustomUser,
    comments: List[Comment],
) -> Set[int]:
    """
    Возвращает множество id комментариев, которые лайкнул пользователь.

    Args:
        user (CustomUser): Пользователь, для которого нужно получить лайкнутые комментарии.
        comments (List[Comment]): Список комментариев для проверки.

    Returns:
        Set[int]: Множество id комментариев, которые лайкнул пользователь.
    """

    comment_ids = [comment.id for comment in comments]
    liked_ids = set(
        Like.objects.filter(user=user, comment_id__in=comment_ids).values_list(
            "comment_id", flat=True
        )
    )

    return liked_ids


def get_comment(comment_id: int) -> Comment:
    """
    Возвращает комментарий по id.

    Args:
        comment_id (int): id комментария, который нужно получить.

    Returns:
        Comment: Комментарий.

    Raises:
        NotFound: Если комментарий не найден.
    """
    comment = (
        Comment.objects.filter(id=comment_id)
        .select_related("author", "thread", "reply_to_author")
        .first()
    )
    if not comment:
        raise NotFound()
    return comment


def get_post_comments(post_id: int, user: CustomUser) -> QuerySet:
    """
    Возвращает все комментарии к посту.

    Args:
        post_id (int): id поста, к которому нужно получить комментарии.
        user (CustomUser): Пользователь для отметки лайков.

    Returns:
        QuerySet: Комментарии к посту.
    """
    comments = Comment.objects.filter(
        post_id=post_id, thread__isnull=True
    ).select_related("author")
    liked_ids = get_user_liked_current_comment_ids(user=user, comments=comments)

    for comment in comments:
        comment.is_liked_by_user = comment.id in liked_ids

    return comments


def get_comment_replies(comment_id: int, user: CustomUser) -> QuerySet:
    """
    Возвращает все ответы к комментарию.

    Args:
        comment_id (int): id комментария, к которому нужно получить ответы.
        user (CustomUser): Пользователь для отметки лайков.

    Returns:
        QuerySet: Ответы к комментарию.
    """
    replies = Comment.objects.filter(thread_id=comment_id).select_related(
        "author", "reply_to", "reply_to_author"
    )
    liked_ids = get_user_liked_current_comment_ids(user=user, comments=replies)

    for reply in replies:
        reply.is_liked_by_user = reply.id in liked_ids

    return replies


def get_user_comments(username: str) -> QuerySet:
    """
    Возвращает все комментарии, написанные пользователем.

    Args:
        username (str): username пользователя, чьи комментарии нужно получить.

    Returns:
        QuerySet: Комментарии пользователя.
    """
    return Comment.objects.filter(author__username=username).select_related(
        "author", "reply_to_author"
    )
