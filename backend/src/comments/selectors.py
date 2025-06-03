from rest_framework.exceptions import NotFound
from comments.models import Comment


def get_comment(comment_id: int) -> Comment:
    comment = Comment.objects.filter(id=comment_id).first()

    if not comment:
        raise NotFound()

    return comment
