from typing import Any
from django.core.cache import cache
from rest_framework.exceptions import ValidationError, NotFound
from accounts.models import CustomUser
from accounts.tasks import send_confirmation_email
from profiles.services import create_profile


def register_user(data: dict[str, Any]) -> None:
    user = CustomUser.objects.filter(email=data["email"]).first()
    if user:
        if user.email_verified:
            raise ValidationError({"email": "Этот email уже используется"})

        # Обновить данные, если пользователь неактивен
        user.username = data["username"]
        user.set_password(data["password"])
        user.save()
    else:
        user = CustomUser.objects.create_user(**data)

    send_confirmation_email.delay(user.email)

    return None


def confirm_code(data: dict[str, Any]) -> None:
    email = data["email"]
    code = data["code"]

    user = CustomUser.objects.filter(email=email).first()

    if not user:
        raise NotFound(detail="Пользователь не найден")

    if user.email_verified:
        raise ValidationError(detail="Почта уже подтверждена")

    real_code = cache.get(email)

    if real_code is None:
        raise ValidationError(
            detail="Код истёк или не запрашивался",
        )

    if code != real_code:
        raise ValidationError(detail="Неверный код")

    user.email_verified = True
    user.save()

    create_profile(user)
    cache.delete(email)
