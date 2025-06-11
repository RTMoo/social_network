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
        raise ValidationError({"to_user": "Вы уже запрашивали дружбу"})
