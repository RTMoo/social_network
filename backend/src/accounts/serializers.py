from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError,
)
from accounts.models import CustomUser
from accounts.tasks import send_confirmation_email


class UserRegistrationSerializer(ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    email = EmailField(required=True)
    username = CharField(required=True)
    password = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def validate(self, data):
        user = CustomUser.objects.filter(email=data["email"]).first()
        if user and user.is_active:
            raise ValidationError({"email": "Этот email уже используется"})
        return data

    def create(self, validated_data):
        email = validated_data["email"]

        user = CustomUser.objects.filter(email=email).first()
        if user:
            # Обновить данные, если пользователь неактивен (например, username или пароль)
            user.username = validated_data["username"]
            user.set_password(validated_data["password"])
            user.save()
        else:
            user = CustomUser.objects.create_user(**validated_data)

        send_confirmation_email.delay(email=email)
        return user


class UserConfirmCodeSerializer(Serializer):
    email = EmailField()
    code = CharField()
