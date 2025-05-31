from typing import Any
from posts.models import Post
from accounts.models import CustomUser


def create_post(data: dict[str, Any], author: CustomUser) -> Post:
    post = Post.objects.create(**data, author=author)

    return post
