from rest_framework.exceptions import NotFound
from posts.models import Post
from subscriptions.selectors import get_user_subscriptions


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


def get_subscription_posts(username: str):
    subscriptions = get_user_subscriptions(username=username)

    posts = (
        Post.objects.filter(author__username__in=subscriptions)
        .select_related("author")
        .all()
    )

    return posts
