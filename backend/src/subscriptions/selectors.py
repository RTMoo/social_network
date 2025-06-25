from accounts.models import CustomUser
from subscriptions.models import Subscription
from rest_framework.exceptions import NotFound
from typing import List


def get_subscribe(sender: CustomUser, username: str) -> Subscription:
    """
    Возвращает объект подписки.

    Args:
        sender (CustomUser): Пользователь, который подписан.
        username (str): Имя пользователя, на которого оформлена подписка.

    Returns:
        Subscription: Объект подписки.

    Raises:
        NotFound: Если подписка не найдена.
    """

    subscription = Subscription.objects.filter(
        subscriber=sender,
        to_subscribe__username=username,
    ).first()

    if not subscription:
        raise NotFound(detail="Подписка не найдена.")

    return subscription


def get_user_subscriptions(username: str) -> List[str]:
    """
    Возвращает список username пользователей, на которых подписан переданный пользователь.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[str]: Список username пользователей.
    """

    subscriptions = (
        Subscription.objects.filter(subscriber__username=username)
        .select_related("to_subscribe")
        .all()
    )

    return [subscribe.to_subscribe.username for subscribe in subscriptions]


def get_user_subscribers(username: str) -> List[str]:
    """
    Возвращает список username пользователей, которые подписаны на переданного пользователя.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[str]: Список username пользователей.
    """

    subscribers = (
        Subscription.objects.filter(to_subscribe__username=username)
        .select_related("subscriber")
        .all()
    )

    return [subscribe.subscriber.username for subscribe in subscribers]
