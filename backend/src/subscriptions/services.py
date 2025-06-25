from django.db import IntegrityError, transaction

from accounts.models import CustomUser
from accounts.selectors import get_user
from subscriptions.models import Subscription
from subscriptions.selectors import get_subscribe
from rest_framework.exceptions import ValidationError
from subscriptions.utils import increment_subscribe_count, decrement_subscribe_count


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

    to_subscribe = get_user(username=username)

    try:
        with transaction.atomic():
            Subscription.objects.create(subscriber=sender, to_subscribe=to_subscribe)
            increment_subscribe_count(sender=sender, to_subscribe=to_subscribe)
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

    subscription = get_subscribe(subscriber=sender.username, to_subscribe=username)

    to_subscribe = subscription.to_subscribe

    with transaction.atomic():
        subscription.delete()
        decrement_subscribe_count(sender=sender, to_subscribe=to_subscribe)


def delete_subscriber(sender: CustomUser, username: str) -> None:
    """
    Удаляет пользователя из списка подписчиков.
    """
    subscriber = get_user(username=username)
    subscription = get_subscribe(subscriber=username, to_subscribe=sender.username)

    with transaction.atomic():
        subscription.delete()
        decrement_subscribe_count(sender=subscriber, to_subscribe=sender)
