from typing import Any
from rest_framework.exceptions import PermissionDenied
from posts.models import Post
from accounts.models import CustomUser
from posts.selectors import get_post


def create_post(data: dict[str, Any], author: CustomUser) -> Post:
    post = Post.objects.create(**data, author=author)

    return post


def update_post(data: dict[str, Any], post_id: int) -> Post:
    post = get_post(post_id)

    for key, value in data.items():
        setattr(post, key, value)

    post.save()

    return post


def delete_post(post_id: int, author: CustomUser) -> None:
    post = get_post(post_id)

    if post.author != author:
        raise PermissionDenied()

    post.delete()
