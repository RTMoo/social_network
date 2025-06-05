from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    post_id = serializers.IntegerField()
    thread_id = serializers.IntegerField(read_only=True)
    reply_to_id = serializers.IntegerField(required=False, allow_null=True)
    reply_to_author = serializers.CharField(read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)
    text = serializers.CharField(max_length=256)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CommentUpdateSerializer(serializers.Serializer):
    reply_to_id = serializers.IntegerField(required=False, allow_null=True)
    text = serializers.CharField(max_length=256)
