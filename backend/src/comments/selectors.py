from rest_framework.exceptions import NotFound
from comments.models import Comment


def get_comment(comment_id: int) -> Comment:
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
    Возвращает комментарии первого уровня
    """

    return Comment.objects.filter(post_id=post_id, thread__isnull=True).select_related(
        "author"
    )


def get_comment_replies(comment_id: int):
    """
    Возвращает все ответы под родительским комментарием
    """

    return Comment.objects.filter(thread_id=comment_id).select_related(
        "author", "reply_to", "reply_to_author"
    )


def get_user_comments(username: str):
    return Comment.objects.filter(author__username=username).select_related(
        "author", "reply_to_author"
    )
