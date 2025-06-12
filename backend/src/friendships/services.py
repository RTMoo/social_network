from typing import Any
from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from accounts.selectors import get_user
from accounts.models import CustomUser
from friendships.models import FriendshipRequest, Friendship
from friendships.selectors import get_friendship_request, friend_exists, request_exists


def create_friendship_request(
    from_user: CustomUser,
    data: dict[str, Any],
) -> FriendshipRequest:
    """
    Создаёт запрос на дружбу от from_user к пользователю с username из data.

    Проверки:
    - Если пользователи уже друзья — ошибка.
    - Если существует обратный запрос на дружбу — ошибка.
    - Если запрос уже существует в этом направлении — IntegrityError, обрабатывается как ошибка.

    Args:
        from_user (CustomUser): Пользователь, отправляющий запрос.
        data (dict[str, Any]): Словарь, содержащий ключ "to_user" с username получателя.

    Returns:
        FriendshipRequest: Созданный объект запроса на дружбу.

    Raises:
        ValidationError: Если запрос недопустим (дружба уже есть или запрос уже отправлен).
    """

    to_user = get_user(username=data["to_user"])

    if friend_exists(user1=from_user, user2=to_user):
        raise ValidationError({"to_user": f"Вы уже дружите с {to_user.username}"})

    if request_exists(to_user=from_user, from_user=to_user):
        raise ValidationError(
            {"to_user": f"{to_user.username} уже отправил(а) вам запрос"}
        )

    try:
        with transaction.atomic():
            request = FriendshipRequest.objects.create(
                from_user=from_user, to_user=to_user
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
    """
    Создаёт запрос на дружбу от from_user к пользователю с username из data.

    Проверяет:
    - Если пользователи уже друзья — ошибка.
    - Если есть обратный запрос — ошибка.
    - Если запрос уже существует — ошибка через IntegrityError.

    Args:
        from_user (CustomUser): Пользователь, отправляющий запрос.
        data (dict[str, Any]): Словарь с ключом "to_user" (username получателя).

    Returns:
        FriendshipRequest: Созданный запрос на дружбу.

    Raises:
        ValidationError: Если запрос недопустим.
    """

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
