from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    post_id = serializers.IntegerField()
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    author = serializers.CharField(source="author.username", read_only=True)
    text = serializers.CharField(max_length=256)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
