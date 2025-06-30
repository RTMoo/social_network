from typing import List
from notifications.models import Notification
from notifications.selectors import get_user_notification, get_user_notification_list


def get_user_notifications_service(
    username: str,
    is_read: bool = False,
) -> List[Notification]:
    """
    Получает уведомления пользователя с фильтрацией по статусу прочтения.

    Args:
        username (str): Имя пользователя
        is_read (bool, optional): Фильтр по статусу прочтения. None - все уведомления

    Returns:
        List[Notification]: Список уведомлений
    """

    return get_user_notification_list(username=username, is_read=is_read)


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
