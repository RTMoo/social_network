from rest_framework import serializers


class CreateChatSerializer(serializers.Serializer):
    to_user = serializers.CharField()


class ChatSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField(source="id")
    second_user = serializers.CharField(source="second_user.username")
    last_message = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_last_message(self, obj):
        return obj.last_message.text if obj.last_message else None


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    chat_id = serializers.IntegerField()
    text = serializers.CharField()
    author = serializers.CharField(source="author.username")
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
