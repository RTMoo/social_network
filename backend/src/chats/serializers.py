from rest_framework import serializers


class CreateChatSerializer(serializers.Serializer):
    to_user = serializers.CharField()


class ChatSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField(source="id")
    second_user = serializers.CharField(source="second_user.username")
    last_message = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_last_message(self, obj):
        if obj.last_message:
            return {
                "text": obj.last_message.text,
                "author": obj.last_message.author.username
                if obj.last_message.author
                else None,
                "created_at": obj.last_message.created_at,
            }
        return None


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    chat_id = serializers.IntegerField()
    text = serializers.CharField()
    author = serializers.CharField(source="author.username")
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
