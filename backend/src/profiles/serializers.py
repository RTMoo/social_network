from rest_framework import serializers
from profiles.validators import validate_min_length_if_not_empty


class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=32, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=32, allow_blank=True, required=False)
    avatar = serializers.ImageField(allow_null=True, required=False)
    bio = serializers.CharField(max_length=512, allow_blank=True, required=False)
    birth_date = serializers.DateField(allow_null=True, required=False)
    country = serializers.CharField(max_length=2, allow_blank=True, required=False)

    def validate_first_name(self, value):
        validate_min_length_if_not_empty("first_name", value)
        return value

    def validate_last_name(self, value):
        validate_min_length_if_not_empty("last_name", value)
        return value
