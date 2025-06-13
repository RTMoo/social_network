from friendships.models import FriendshipRequest, Friendship
from friendships.utils import sort_models
from rest_framework.exceptions import NotFound
from django.db.models import Q
from accounts.models import CustomUser


def get_friendship_request(
    from_user,
    to_user,
) -> FriendshipRequest:
    """
    Возвращает запрос на дружбу между двумя пользователями.
    """

    request = FriendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user
    ).first()

    if not request:
        raise NotFound(detail="Запрос дружбы не найден")

    return request


def friend_exists(
    user1: CustomUser,
    user2: CustomUser,
) -> bool:
    """
    Проверяет, существует ли дружба между двумя пользователями.
    """

    user1, user2 = sort_models([user1, user2])

    return Friendship.objects.filter(user1=user1, user2=user2).exists()


def get_friendship_request_between(
    from_user: CustomUser,
    to_user: CustomUser,
) -> FriendshipRequest | None:
    """
    Возвращает запрос на дружбу между двумя пользователями.
    """

    return FriendshipRequest.objects.filter(
        Q(from_user=from_user, to_user=to_user)
        | Q(from_user=to_user, to_user=from_user)
    ).first()
