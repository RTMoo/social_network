from django.db import IntegrityError

from accounts.models import CustomUser
from accounts.selectors import get_user
from subscriptions.models import Subscription
from subscriptions.selectors import get_subscribe
from rest_framework.exceptions import ValidationError


def subscribe(sender: CustomUser, username: str) -> None:
    """
    Создаёт подписку на другого пользователя.

    Args:
        sender (CustomUser): Пользователь, который подписывается.
        username (str): Имя пользователя, на которого нужно подписаться.

    Raises:
        ValidationError: Если пользователь пытается подписаться
                        на самого себя или подписка уже существует.
        NotFound: Если пользователь с переданным username не найден.
    """

    if sender.username == username:
        raise ValidationError("Нельзя подписаться на самого себя.")

    author = get_user(username=username)

    try:
        Subscription.objects.create(subscriber=sender, author=author)
    except IntegrityError:
        raise ValidationError("Подписка уже существует.")


def unsubscribe(sender: CustomUser, username: str) -> None:
    """
    Удаляет подписку на другого пользователя.

    Args:
        sender (CustomUser): Пользователь, который отписывается.
        username (str): Имя пользователя, от которого нужно отписаться.

    Raises:
        ValidationError: Если пользователь пытается отписаться от самого себя.
        NotFound: Если подписка не найдена.
    """

    if sender.username == username:
        raise ValidationError("Нельзя отписаться от самого себя.")

    subscription = get_subscribe(sender=sender, username=username)

    subscription.delete()
