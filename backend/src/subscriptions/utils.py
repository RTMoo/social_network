from accounts.models import CustomUser
from django.db import transaction
from django.db.models import F
from profiles.models import Profile


def increment_subscribe_count(sender: CustomUser, to_subscribe: CustomUser) -> None:
    """
    Увеличивает количество подписок у отправителя и количество подписчиков у получателя.
    """

    with transaction.atomic():
        Profile.objects.filter(user=sender).update(
            subscription_count=F("subscription_count") + 1
        )
        Profile.objects.filter(user=to_subscribe).update(
            subscribers_count=F("subscribers_count") + 1
        )


def decrement_subscribe_count(sender: CustomUser, to_subscribe: CustomUser) -> None:
    """
    Уменьшает количество подписок у отправителя и количество подписчиков у получателя.
    """

    with transaction.atomic():
        Profile.objects.filter(user=sender).update(
            subscription_count=F("subscription_count") - 1
        )
        Profile.objects.filter(user=to_subscribe).update(
            subscribers_count=F("subscribers_count") - 1
        )
