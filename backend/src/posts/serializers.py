from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    author = serializers.CharField(source="author.username", read_only=True)
    title = serializers.CharField(max_length=128)
    content = serializers.CharField(max_length=2000)
    image = serializers.ImageField(required=False, allow_null=True)
    likes_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
