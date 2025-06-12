from typing import Any

from accounts.selectors import get_user
from accounts.models import CustomUser
from friendships.models import FriendshipRequest
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


def create_friendship_request(
    from_user: CustomUser,
    data: dict[str, Any],
) -> FriendshipRequest:
    to_user = get_user(username=data["to_user"])

    try:
        request = FriendshipRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
        )

        return request
    except IntegrityError:
        raise ValidationError(
            {"to_user": f"Вы уже запрашивали дружбу для {to_user.username}"}
        )


def create_friendship(
    to_user: CustomUser,
    data: dict[str, Any],
) -> Friendship:
    from_user = get_user(username=data["from_user"])
    request = get_friendship_request(to_user=to_user, from_user=from_user)

    # Сортировка по ключу если чтобы исключить случай когда A=B и B=A
    user1, user2 = sorted([to_user, from_user], key=lambda user: user.pk)

    try:
        with transaction.atomic():
            friendship = Friendship.objects.create(
                user1=user1,
                user2=user2,
            )
            request.delete()

        return friendship
    except IntegrityError:
        raise ValidationError({"from_user": f"Вы уже дружите с {from_user.username}"})
