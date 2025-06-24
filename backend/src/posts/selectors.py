from rest_framework.exceptions import NotFound
from posts.models import Post
from subscriptions.selectors import get_user_subscriptions
from likes.models import Like
from accounts.models import CustomUser


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


def get_all_posts(user: CustomUser):
    posts = Post.objects.select_related("author").all()
    post_ids = [p.id for p in posts]
    liked_ids = set(
        Like.objects.filter(user=user, post_id__in=post_ids).values_list(
            "post_id", flat=True
        )
    )
    for post in posts:
        post.is_liked_by_user = post.id in liked_ids

    return posts
