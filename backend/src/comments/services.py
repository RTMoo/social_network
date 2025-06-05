from typing import Any
from accounts.models import CustomUser
from comments.models import Comment
from posts.selectors import get_post
from comments.selectors import get_comment
from rest_framework.exceptions import ValidationError


def create_comment(
    data: dict[str, Any],
    author: CustomUser,
) -> Comment:
    post = get_post(post_id=data.get("post_id"))

    thread = None
    reply_to_comment = None

    thread_id = data.get("thread_id")
    reply_to_id = data.get("reply_to_id")

    # Проверяем thread (верхний комментарий ветки)
    if thread_id is not None:
        thread_comment = get_comment(comment_id=thread_id)
        if thread_comment.post_id != post.id:
            raise ValidationError(
                {"thread_id": "Комментарий thread не принадлежит данному посту."}
            )
        # thread — всегда самый верхний в ветке
        if thread_comment.thread_id is not None:
            thread = thread_comment.thread_id
        else:
            thread = thread_comment

    # Проверяем reply_to (конкретный коммент, на который отвечаем)
    if reply_to_id is not None:
        reply_to_comment = get_comment(comment_id=reply_to_id)
        if reply_to_comment.post_id != post.id:
            raise ValidationError(
                {"reply_to": "Комментарий reply_to не принадлежит данному посту."}
            )
        # reply_to может быть любым комментом в этой ветке

    comment = Comment.objects.create(
        post=post,
        author=author,
        thread=thread,
        reply_to=reply_to_comment,
        text=data.get("text"),
    )

    return comment
