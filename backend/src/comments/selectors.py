from rest_framework.exceptions import NotFound
from comments.models import Comment


def get_comment(comment_id: int) -> Comment:
    """
    Возвращает комментарий по id.

    Args:
        comment_id: int - id комментария, который нужно получить

    Returns:
        Comment - комментарий

    Raises:
        NotFound: если комментарий не найден
    """

    comment = (
        Comment.objects.filter(id=comment_id)
        .select_related("author", "thread", "reply_to_author")
        .first()
    )

    if not comment:
        raise NotFound()

    return comment


def get_post_comments(post_id: int):
    """
    Возвращает все комментарии к посту.

    Args:
        post_id: int - id поста, к которому нужно получить комментарии

    Returns:
        Queryset[Comment] - комментарии
    """

    return Comment.objects.filter(post_id=post_id, thread__isnull=True).select_related(
        "author"
    )


def get_comment_replies(comment_id: int):
    """
    Возвращает все ответы к комментарию.

    Args:
        comment_id: int - id комментария, к которому нужно получить ответы

    Returns:
        Queryset[Comment] - ответы
    """

    return Comment.objects.filter(thread_id=comment_id).select_related(
        "author", "reply_to", "reply_to_author"
    )


def get_user_comments(username: str):
    """
    Возвращает все комментарии, написанные пользователем.

    Args:
        username: str - username пользователя, чьи комментарии нужно получить

    Returns:
        Queryset[Comment] - комментарии
    """

    return Comment.objects.filter(author__username=username).select_related(
        "author", "reply_to_author"
    )
