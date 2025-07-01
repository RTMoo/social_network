from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    from_user = serializers.CharField(read_only=True, source="from_user.username")
    to_user = serializers.CharField(read_only=True, source="to_user.username")
    type = serializers.ChoiceField(choices=Notification.Types.choices)
    created_at = serializers.DateTimeField(read_only=True)
    is_read = serializers.BooleanField(read_only=True)
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)
    post_preview = serializers.ImageField(source="post.preview", read_only=True)
    comment_id = serializers.IntegerField(source="comment.id", read_only=True)
    comment_text = serializers.CharField(source="comment.text", read_only=True)
