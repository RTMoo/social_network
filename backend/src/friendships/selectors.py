from friendships.models import FriendshipRequest, Friendship
from rest_framework.exceptions import NotFound


def get_friendship_request(from_user, to_user) -> FriendshipRequest:
    """
    Возвращает запрос на дружбу между двумя пользователями.
    """

    request = FriendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user
    ).first()

    if not request:
        raise NotFound(detail="Запрос дружбы не найден")

    return request


def friend_exists(user1, user2) -> bool:
    """
    Проверяет, существует ли дружба между двумя пользователями.
    """

    user1, user2 = sorted([user1, user2], key=lambda user: user.pk)

    return Friendship.objects.filter(user1=user1, user2=user2).exists()


def request_exists(from_user, to_user) -> bool:
    """
    Проверяет, существует ли запрос на дружбу от from_user к to_user.
    """

    return FriendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user
    ).exists()
