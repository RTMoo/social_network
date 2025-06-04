from rest_framework.exceptions import NotFound
from comments.models import Comment


def get_comment(comment_id: int) -> Comment:
    comment = Comment.objects.filter(id=comment_id).first()

    if not comment:
        raise NotFound()

    return comment


def get_post_comments(post_id: int):
    """
    Возвращает комментарии первого уровня
    """

    return Comment.objects.filter(post_id=post_id, parent__isnull=True)


def get_comment_replies(comment_id: int):
    """
    Возвращает все ответы под родительским комментарием
    """

    return Comment.objects.filter(parent_id=comment_id)
