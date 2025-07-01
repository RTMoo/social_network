from celery import shared_task
from subscriptions.selectors import get_user_subscribers
from notifications.models import Notification
from accounts.selectors import get_user
from posts.selectors import get_post


@shared_task
def notify_subscribers_about_new_post(post_author_username: str, post_id: int) -> None:
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
