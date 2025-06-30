from django.urls import path
from notifications.views import (
    get_notifications,
    mark_as_read,
    delete_notification_view,
)

urlpatterns = [
    path(
        route="",
        view=get_notifications,
        name="get_notifications",
    ),
    path(
        route="<int:notification_id>/mark-read/",
        view=mark_as_read,
        name="mark_as_read",
    ),
    path(
        route="<int:notification_id>/delete/",
        view=delete_notification_view,
        name="delete_notification",
    ),
]
