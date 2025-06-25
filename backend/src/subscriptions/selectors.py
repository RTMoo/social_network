from accounts.models import CustomUser
from profiles.models import Profile
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


def subscribe_exists(sender: CustomUser, username: str) -> bool:
    """
    Проверяет, существует ли подписка между двумя пользователями.
    """
    return Subscription.objects.filter(
        subscriber=sender, to_subscribe__username=username
    ).exists()


def get_user_subscriptions(username: str) -> List[Profile]:
    """
    Возвращает список профилей пользователей, на которых подписан переданный пользователь.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[Profile]: Список профилей пользователей.
    """

    subscriptions = (
        Subscription.objects.filter(subscriber__username=username)
        .select_related("to_subscribe__profile")
        .all()
    )

    return [subscribe.to_subscribe.profile for subscribe in subscriptions]


def get_user_subscribers(username: str) -> List[Profile]:
    """
    Возвращает список профилей пользователей, которые подписаны на переданного пользователя.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[Profile]: Список профилей пользователей.
    """

    subscribers = (
        Subscription.objects.filter(to_subscribe__username=username)
        .select_related("subscriber")
        .all()
    )

    return [subscribe.subscriber.profile for subscribe in subscribers]
