from notifications.models import Notification
from notifications.selectors import get_user_notification


def mark_notification_as_read(notification_id: int, username: str) -> Notification:
    """
    Отмечает уведомление как прочитанное.

    Args:
        notification_id (int): ID уведомления
        username (str): Имя пользователя для проверки прав доступа

    Returns:
        Notification: Обновленное уведомление

    Raises:
        NotFound: Если уведомление не найдено или не принадлежит пользователю
    """
    notification = get_user_notification(
        notification_id=notification_id,
        username=username,
    )

    notification.is_read = True
    notification.save()

    return notification


def delete_notification(notification_id: int, username: str) -> None:
    """
    Удаляет уведомление.

    Args:
        notification_id (int): ID уведомления
        username (str): Имя пользователя для проверки прав доступа

    Raises:
        NotFound: Если уведомление не найдено или не принадлежит пользователю
    """
    notification = get_user_notification(
        notification_id=notification_id, username=username
    )

    notification.delete()
