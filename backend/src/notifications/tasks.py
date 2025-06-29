from celery import shared_task
from subscriptions.selectors import get_user_subscribers
from notifications.models import Notification
from accounts.selectors import get_user


@shared_task
def notify_subscribers_about_new_post(post_author_username: str) -> None:
    post_author = get_user(username=post_author_username)

    subscribers = get_user_subscribers(username=post_author_username)

    notifications = [
        Notification(
            from_user=post_author,
            to_user=subscriber,
            type=Notification.Types.NEW_POST,
        )
        for subscriber in subscribers
    ]

    Notification.objects.bulk_create(notifications, batch_size=1000)
