from typing import Any
from accounts.models import CustomUser
from comments.models import Comment
from posts.selectors import get_post
from comments.selectors import get_comment
from rest_framework.exceptions import ValidationError


def create_comment(data: dict[str, Any], author: CustomUser) -> Comment:
    post = get_post(post_id=data.get("post_id"))

    parent = None
    parent_id = data.get("parent_id")

    if parent_id is not None:
        parent_comment = get_comment(comment_id=parent_id)

        if parent_comment.post_id != post.id:
            raise ValidationError(
                {"parent_id": "Родительский комментарий не принадлежит данному посту."}
            )

        # если parent_comment — это ответ, берём его parent_id
        if parent_comment.parent is not None:
            parent = parent_comment.parent
        else:
            parent = parent_comment

    comment = Comment.objects.create(
        post=post,
        author=author,
        parent=parent,
        text=data.get("text"),
    )

    return comment
