from typing import Any
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
