from friendships.models import FriendshipRequest, Friendship
from friendships.utils import sort_models
from rest_framework.exceptions import NotFound
from django.db.models import Q, QuerySet
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


def get_friendship_usernames(
    username: str,
) -> list[str]:
    """
    Возвращает список username друзей пользователя.
    """
    friendships = Friendship.objects.filter(
        Q(user1__username=username) | Q(user2__username=username)
    ).select_related(
        "user1",
        "user2",
    )

    return [
        friend.user2.username
        if friend.user1.username == username
        else friend.user1.username
        for friend in friendships
    ]


def get_sent_friendship_requests(
    sender: CustomUser,
) -> QuerySet[FriendshipRequest]:
    """
    Возвращает запросы на дружбу отправленные пользователем.
    """

    return FriendshipRequest.objects.filter(from_user=sender).select_related(
        "from_user",
        "to_user",
    )


def get_received_friendship_requests(
    recipient: CustomUser,
) -> QuerySet[FriendshipRequest]:
    """
    Возвращает запросы на дружбу полученные пользователем.
    """

    return FriendshipRequest.objects.filter(to_user=recipient).select_related(
        "from_user",
        "to_user",
    )


def get_friendship(
    user1: CustomUser,
    user2: CustomUser,
) -> Friendship | None:
    """
    Возвращает дружбу между двумя пользователями.
    """

    user1, user2 = sort_models([user1, user2])

    return Friendship.objects.filter(user1=user1, user2=user2).first()
