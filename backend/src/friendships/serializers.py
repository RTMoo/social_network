from rest_framework import serializers


class FriendshipRequestSerializer(serializers.Serializer):
    from_user = serializers.CharField(source="from_user.username")
    to_user = serializers.CharField(source="to_user.username")
    created_at = serializers.DateTimeField()
