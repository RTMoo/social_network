from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError, NotFound
from accounts.selectors import get_user
from accounts.models import CustomUser
from friendships.models import FriendshipRequest, Friendship
from friendships import selectors
from friendships.utils import sort_models


def send_friendship_request(
    current_user: CustomUser,
    username: str,
) -> FriendshipRequest:
    """
    Создаёт запрос на дружбу от текущего пользователя к пользователю с username.

    Проверки:
    - Если пользователи уже друзья — ошибка.
    - Если существует обратный запрос на дружбу — ошибка.
    - Если запрос уже существует в этом направлении — IntegrityError, обрабатывается как ошибка.

    Args:
        from_user (CustomUser): Пользователь, отправляющий запрос.
        username: username получателя.

    Returns:
        FriendshipRequest: Созданный объект запроса на дружбу.

    Raises:
        ValidationError: Если запрос недопустим (дружба уже есть или запрос уже отправлен).
    """

    to_user = get_user(username=username)

    if current_user.username == username:
        raise ValidationError({"to_user": "Нельзя отправить запрос самому себе"})

    if selectors.friend_exists(user1=current_user, user2=to_user):
        raise ValidationError({"to_user": f"Вы уже дружите с {username}"})

    request = selectors.get_friendship_request_between(
        from_user=current_user, to_user=to_user
    )

    if request is not None:
        if request.to_user == to_user:
            raise ValidationError(
                {"to_user": f"Вы уже отправили запрос на дружбу для {username}"}
            )
        else:
            raise ValidationError({"to_user": f"{username} уже отправил(а) вам запрос"})

    try:
        with transaction.atomic():
            request = FriendshipRequest.objects.create(
                from_user=current_user, to_user=to_user
            )

            return request

    except IntegrityError:
        raise ValidationError(
            {"to_user": f"Вы уже отправили запрос на дружбу для {to_user.username}"}
        )


def accept_friendship_request(
    to_user: CustomUser,
    username: str,
) -> Friendship:
    """
    Принимает запрос на дружбу от пользователя с username и создаёт объект дружбы.

    Args:
        to_user (CustomUser): Пользователь, принимающий запрос.
        from_username (str): Username пользователя, отправившего запрос.

    Returns:
        Friendship: Объект дружбы между двумя пользователями.

    Raises:
        ValidationError: Если дружба уже существует.
        NotFound: Если запрос не найден.
    """

    from_user = get_user(username=username)
    request = selectors.get_friendship_request(to_user=to_user, from_user=from_user)

    user1, user2 = sort_models([from_user, to_user])

    try:
        with transaction.atomic():
            friendship = Friendship.objects.create(user1=user1, user2=user2)
            request.delete()
            return friendship

    except IntegrityError:
        raise ValidationError({"from_user": f"Вы уже дружите с {from_user.username}"})


def reject_friendship_request(
    current_user: CustomUser,
    username: str,
) -> None:
    """
    Отклоняет (удаляет) запрос на дружбу между текущим пользователем и другим.

    Args:
        current_user (CustomUser): Пользователь, отклоняющий запрос.
        other_username (str): Username второго пользователя.

    Raises:
        NotFound: Если запрос на дружбу не существует.
    """

    to_user = get_user(username=username)
    request = selectors.get_friendship_request_between(
        from_user=current_user, to_user=to_user
    )

    if not request:
        raise NotFound(detail="Запрос дружбы не найден")

    request.delete()


def delete_friendship(current_user: CustomUser, username: str) -> None:
    """
    Удаляет дружбу между текущим пользователем и другим.

    Args:
        current_user (CustomUser): Пользователь, удаляющий дружбу.
        username (str): Username второго пользователя.

    Raises:
        NotFound: Если дружба не существует.
    """

    to_user = get_user(username=username)
    friendship = selectors.get_friendship(user1=current_user, user2=to_user)

    if not friendship:
        raise NotFound(detail="Вы не состоите в дружбе с этим пользователем.")

    friendship.delete()
