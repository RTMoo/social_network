from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)
    title = serializers.CharField(
        max_length=128,
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    content = serializers.CharField(
        max_length=2000,
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    image = serializers.ImageField()
    preview = serializers.ImageField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
