from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.serializers import NotificationSerializer
from notifications.services import (
    get_user_notifications_service,
    mark_notification_as_read,
    delete_notification,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """
    Получает уведомления пользователя с возможностью фильтрации по статусу прочтения.

    Query параметры:
    - is_read: true/false для фильтрации по статусу прочтения
    """

    is_read_param = request.query_params.get("is_read")

    # Преобразуем строку в boolean
    is_read = None
    if is_read_param is not None:
        is_read = is_read_param.lower() == "true"

    notifications = get_user_notifications_service(
        username=request.user.username,
        is_read=is_read,
    )

    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """
    Отмечает уведомление как прочитанное.
    """

    notification = mark_notification_as_read(
        notification_id=notification_id, username=request.user.username
    )
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_notification_view(request, notification_id):
    """
    Удаляет уведомление.
    """

    delete_notification(notification_id=notification_id, username=request.user.username)
    return Response(status=status.HTTP_204_NO_CONTENT)
