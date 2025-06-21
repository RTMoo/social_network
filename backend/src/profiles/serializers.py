from rest_framework import serializers
from profiles.validators import validate_min_length_if_not_empty
from django_countries.serializer_fields import CountryField


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True, source="user.username")
    email = serializers.EmailField(read_only=True, source="user.email")
    first_name = serializers.CharField(max_length=32, required=False)
    last_name = serializers.CharField(max_length=32, required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(max_length=512, required=False, allow_null=True, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    country = CountryField(country_dict=True, required=False, allow_null=True)

    def validate_first_name(self, value):
        validate_min_length_if_not_empty("first_name", value)
        return value

    def validate_last_name(self, value):
        validate_min_length_if_not_empty("last_name", value)
        return value
