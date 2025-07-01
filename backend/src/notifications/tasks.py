from celery import shared_task
from django.db import IntegrityError
from subscriptions.selectors import get_user_subscribers
from notifications.models import Notification
from accounts.selectors import get_user
from posts.selectors import get_post


@shared_task
def notify_subscribers_about_new_post(post_author_username: str, post_id: int) -> None:
    """
    Уведомляет всех подписчиков о новом посте.

    Args:
        post_author_username (str): username автора поста.
        post_id (int): id поста.
    """

    post = get_post(post_id=post_id)
    post_author = get_user(username=post_author_username)
    subscribers = get_user_subscribers(username=post_author_username)

    notifications = [
        Notification(
            from_user=post_author,
            to_user=subscriber,
            type=Notification.Types.NEW_POST,
            post=post,
        )
        for subscriber in subscribers
    ]

    Notification.objects.bulk_create(notifications, batch_size=1000)


@shared_task
def notify_user_about_new_like(liked_user_username: str, post_id: int) -> None:
    """
    Уведомляет автора поста о новом лайке.

    Args:
        liked_user_username (str): username пользователя, который лайкнул пост.
        post_id (int): id поста.
    """

    post = get_post(post_id=post_id)
    liked_user = get_user(username=liked_user_username)

    if liked_user == post.author:
        return None

    try:
        Notification.objects.create(
            from_user=liked_user,
            to_user=post.author,
            type=Notification.Types.LIKE,
            post=post,
        )
    except IntegrityError:
        return None
