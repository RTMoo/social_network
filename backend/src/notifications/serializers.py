from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    from_user = serializers.CharField(read_only=True, source="from_user.username")
    to_user = serializers.CharField(read_only=True, source="to_user.username")
    type = serializers.ChoiceField(choices=Notification.Types.choices)
    created_at = serializers.DateTimeField(read_only=True)
    is_read = serializers.BooleanField()
