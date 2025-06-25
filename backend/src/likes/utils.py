from posts.models import Post
from comments.models import Comment
from typing import Union


def change_likes_count(obj: Union[Post, Comment], increment: bool = True) -> None:
    """
    Изменяет количество лайков у объекта Post или Comment.

    Args:
        obj (Union[Post, Comment]): Объект поста или комментария.
        increment (bool, optional): True для увеличения, False для уменьшения. По умолчанию True.
    """
    if increment:
        obj.likes_count += 1
    else:
        obj.likes_count -= 1

    obj.save()
