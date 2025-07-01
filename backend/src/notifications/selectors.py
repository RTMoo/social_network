from typing import List
from notifications.models import Notification
from rest_framework.exceptions import NotFound


def get_user_notification_list(
    username: str,
    is_read: bool = False,
) -> List[Notification]:
    notifications = Notification.objects.filter(
        to_user__username=username,
        is_read=is_read,
    ).select_related("post", "comment", "from_user", "to_user")

    return notifications


def get_user_notification(
    notification_id: int,
    username: str,
) -> Notification:
    notification = Notification.objects.filter(
        id=notification_id,
        to_user__username=username,
    ).first()

    if not notification:
        raise NotFound("Уведомление не найдено")

    return notification
