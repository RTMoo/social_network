from typing import Any
from accounts.models import CustomUser
from comments.models import Comment
from posts.selectors import get_post
from comments.selectors import get_comment
from rest_framework.exceptions import ValidationError, PermissionDenied


def create_comment(
    data: dict[str, Any],
    sender: CustomUser,
) -> Comment:
    """
    Создает новый комментарий.

    Args:
        data: dict со следующими полями:
            post_id: int - id поста, к которомуعلقется комментарий
            reply_to_id: int - id комментария, на который отвечаем (опционально)
            text: str - текст комментария
        author: CustomUser - автор комментария

    Returns:
        Comment - созданный комментарий
    """

    post = get_post(post_id=data.get("post_id"))

    thread = None
    reply_to_comment = None
    reply_to_author = None

    reply_to_id = data.get("reply_to_id")

    # Проверяем reply_to (конкретный коммент, на который отвечаем)
    if reply_to_id is not None:
        reply_to_comment = get_comment(comment_id=reply_to_id)
        if reply_to_comment.post_id != post.id:
            raise ValidationError(
                {"reply_to": "Комментарий reply_to не принадлежит данному посту."}
            )

        if reply_to_comment.thread_id is not None:
            thread = reply_to_comment.thread
        else:
            thread = reply_to_comment
        # храним модель CustomUser чтобы при удалении комментарии можно было узнать автора
        reply_to_author = reply_to_comment.author

    comment = Comment.objects.create(
        post=post,
        author=sender,
        thread=thread,
        reply_to=reply_to_comment,
        reply_to_author=reply_to_author,
        text=data.get("text"),
    )

    return comment


def update_comment(
    data: dict[str, Any],
    comment_id: int,
    sender: CustomUser,
) -> Comment:
    """
    Обновляет существующий комментарий.

    Args:
        data: dict со следующими полями:
            text: str - текст комментария
        comment_id: int - id комментария, который нужно обновить
        author: CustomUser - автор комментария

    Returns:
        Comment - обновленный комментарий

    Raises:
        PermissionDenied: если комментарий не принадлежит отправителю
    """

    comment = get_comment(comment_id=comment_id)

    if comment.author != sender:
        raise PermissionDenied()

    comment.text = data.get("text")
    comment.save()

    return comment


def delete_comment(comment_id: int, sender: CustomUser) -> None:
    """
    Удаляет существующий комментарий.

    Args:
        comment_id: int - id комментария, который нужно удалить
        author: CustomUser - автор комментария

    Raises:
        PermissionDenied: если комментарий не принадлежит отправителю
    """

    comment = get_comment(comment_id=comment_id)

    if comment.author != sender:
        raise PermissionDenied()

    comment.delete()
