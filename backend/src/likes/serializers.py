from rest_framework import serializers


class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=False, allow_null=True)
    comment_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        if bool(data.get("post_id")) == bool(data.get("comment_id")):
            raise serializers.ValidationError(
                "Лайк должен быть либо на пост, либо на комментарий"
            )
        return data
