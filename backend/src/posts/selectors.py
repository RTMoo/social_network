from posts.models import Post
from rest_framework.exceptions import NotFound


def get_user_posts(username: str):
    posts = (
        Post.objects.filter(author__username=username).select_related("author").all()
    )

    return posts


def get_post(post_id: int) -> Post:
    post = Post.objects.filter(id=post_id).first()

    if not post:
        raise NotFound()

    return post
