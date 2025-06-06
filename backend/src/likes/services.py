from typing import Any

from likes.models import Like
from likes.utils import change_likes_count
from accounts.models import CustomUser
from posts.selectors import get_post
from comments.selectors import get_comment


def like_object(data: dict[str, Any], sender: CustomUser) -> None:
    post_id = data.get("post_id")
    comment_id = data.get("comment_id")

    if post_id is not None:
        post = get_post(post_id=post_id)

        liked = Like.objects.filter(post_id=post_id, user=sender).first()
        if liked:
            liked.delete()
            change_likes_count(obj=post, increment=False)

        else:
            Like.objects.create(post=post, user=sender)
            change_likes_count(obj=post, increment=True)

    else:
        comment = get_comment(comment_id=comment_id)

        liked = Like.objects.filter(comment_id=comment_id, user=sender).first()
        if liked:
            liked.delete()
            change_likes_count(obj=comment, increment=False)
        else:
            Like.objects.create(comment=comment, user=sender)
            change_likes_count(obj=comment, increment=True)
