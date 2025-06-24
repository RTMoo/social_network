from typing import Any

from likes.models import Like
from likes.utils import change_likes_count
from accounts.models import CustomUser
from posts.selectors import get_post
from comments.selectors import get_comment


def like_post(post_id: int, sender: CustomUser) -> dict[str, bool]:
    """
    Создает или удаляет лайк у поста.

    Args:
        post_id: int - id поста
        author: CustomUser - пользователь, который лайкнул
    """

    post = get_post(post_id=post_id)

    liked_post = Like.objects.filter(post_id=post_id, user=sender).first()
    if liked_post:
        liked_post.delete()
        change_likes_count(obj=post, increment=False)

        return {"liked": False}
    else:
        Like.objects.create(post=post, user=sender)
        change_likes_count(obj=post, increment=True)

        return {"liked": True}


def like_comment(comment_id: int, sender: CustomUser) -> dict[str, bool]:
    """
    Создает или удаляет лайк у комментарии.

    Args:
        comment_id: int - id комментарий
        author: CustomUser - пользователь, который лайкнул
    """

    comment = get_comment(comment_id=comment_id)

    liked_comment = Like.objects.filter(comment_id=comment_id, user=sender).first()
    if liked_comment:
        liked_comment.delete()
        change_likes_count(obj=comment, increment=False)

        return {"liked": False}
    else:
        Like.objects.create(comment=comment, user=sender)
        change_likes_count(obj=comment, increment=True)

        return {"liked": True}
