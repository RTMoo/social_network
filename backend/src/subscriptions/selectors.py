from profiles.models import Profile
from subscriptions.models import Subscription
from rest_framework.exceptions import NotFound
from accounts.models import CustomUser
from typing import List


def get_subscription_between(subscriber: str, to_subscribe: str) -> Subscription:
    """
    Возвращает объект подписки между двумя пользователями.

    Args:
        subscriber (str): Имя пользователя, который подписан.
        to_subscribe (str): Имя пользователя, на которого оформлена подписка.

    Returns:
        Subscription: Объект подписки.

    Raises:
        NotFound: Если подписка не найдена.
    """

    subscription = (
        Subscription.objects.filter(
            subscriber__username=subscriber,
            to_subscribe__username=to_subscribe,
        )
        .select_related("to_subscribe", "subscriber")
        .first()
    )

    if not subscription:
        raise NotFound(detail="Подписка между пользователями не найдена.")

    return subscription


def get_subscription(subscription_id: int) -> Subscription:
    """
    Возвращает объект подписки по его id.
    
    Args:
        subscription_id (int): id подписки.

    Returns:
        Subscription: Объект подписки.

    Raises:
        NotFound: Если подписка не найдена.
    """

    subscription = Subscription.objects.filter(id=subscription_id).first()
    
    if not subscription:
        raise NotFound(detail="Подписка не найдена.")

    return subscription


def subscribe_exists(subscriber: str, to_subscribe: str) -> bool:
    """
    Проверяет, существует ли подписка между двумя пользователями.
    """
    return Subscription.objects.filter(
        subscriber__username=subscriber, to_subscribe__username=to_subscribe
    ).exists()


def get_user_subscription_profiles(username: str) -> List[Profile]:
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


def get_user_subscriber_profiles(username: str) -> List[Profile]:
    """
    Возвращает список профилей пользователей, которые подписаны на переданного пользователя.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[Profile]: Список профилей пользователей.
    """

    subscribers = (
        Subscription.objects.filter(to_subscribe__username=username)
        .select_related("subscriber__profile")
        .all()
    )

    return [subscribe.subscriber.profile for subscribe in subscribers]


def get_user_subscribers(username: str) -> List[CustomUser]:
    """
    Возвращает список пользователей, которые подписаны на переданного пользователя.

    Args:
        username (str): Имя пользователя.

    Returns:
        List[CustomUser]: Список пользователей.
    """

    subscribers = (
        Subscription.objects.filter(to_subscribe__username=username)
        .select_related("subscriber")
        .all()
    )

    return [subscribe.subscriber for subscribe in subscribers]
