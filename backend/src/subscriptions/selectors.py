from accounts.models import CustomUser
from subscriptions.models import Subscription
from rest_framework.exceptions import NotFound


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
        subscriber=sender, to_subscribe__username=username
    ).first()

    if not subscription:
        raise NotFound(detail="Подписка не найдена.")

    return subscription
