from friendships.models import FriendshipRequest, Friendship
from friendships.utils import sort_models
from rest_framework.exceptions import NotFound
from django.db.models import Q, QuerySet
from accounts.models import CustomUser
from typing import List, Optional
from profiles.models import Profile


def get_friendship_request(
    from_user: CustomUser,
    to_user: CustomUser,
) -> FriendshipRequest:
    """
    Возвращает запрос на дружбу между двумя пользователями.

    Args:
        from_user (CustomUser): Пользователь, отправивший запрос.
        to_user (CustomUser): Пользователь, получивший запрос.

    Returns:
        FriendshipRequest: Запрос на дружбу.

    Raises:
        NotFound: Если запрос дружбы не найден.
    """
    request = FriendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user
    ).first()

    if not request:
        raise NotFound(detail="Запрос дружбы не найден")

    return request


def friend_exists(
    user1: CustomUser,
    user2: CustomUser,
) -> bool:
    """
    Проверяет, существует ли дружба между двумя пользователями.

    Args:
        user1 (CustomUser): Первый пользователь.
        user2 (CustomUser): Второй пользователь.

    Returns:
        bool: True, если дружба существует, иначе False.
    """
    user1, user2 = sort_models([user1, user2])

    return Friendship.objects.filter(user1=user1, user2=user2).exists()


def friend_request_exists(from_user: CustomUser, to_user: CustomUser) -> bool:
    return FriendshipRequest.objects.filter(
        from_user=from_user,
        to_user=to_user,
    ).exists()


def get_friendship_request_between(
    from_user: CustomUser,
    to_user: CustomUser,
) -> Optional[FriendshipRequest]:
    """
    Возвращает запрос на дружбу между двумя пользователями.

    Args:
        from_user (CustomUser): Первый пользователь.
        to_user (CustomUser): Второй пользователь.

    Returns:
        Optional[FriendshipRequest]: Запрос на дружбу или None.
    """
    return FriendshipRequest.objects.filter(
        Q(from_user=from_user, to_user=to_user)
        | Q(from_user=to_user, to_user=from_user)
    ).first()


def get_user_friendships(
    username: str,
) -> List[Profile]:
    """
    Возвращает список дружб пользователя.

    Args:
        username (str): username пользователя.

    Returns:
        List[Friendship]: Список дружб.
    """
    friendships = Friendship.objects.filter(
        Q(user1__username=username) | Q(user2__username=username)
    ).select_related("user1__profile", "user2__profile")

    profiles = []

    for friend in friendships:
        if friend.user1.username == username:
            profiles.append(friend.user2.profile)
        else:
            profiles.append(friend.user1.profile)

    return profiles


def get_sent_friendship_requests(
    sender: CustomUser,
) -> List[FriendshipRequest]:
    """
    Возвращает запросы на дружбу отправленные пользователем.

    Args:
        sender (CustomUser): Пользователь, отправивший запросы.

    Returns:
        List[FriendshipRequest]: Запросы на дружбу.
    """
    requests = FriendshipRequest.objects.filter(from_user=sender).select_related(
        "to_user__profile",
    )

    return [request.to_user.profile for request in requests]


def get_received_friendship_requests(
    recipient: CustomUser,
) -> QuerySet[FriendshipRequest]:
    """
    Возвращает запросы на дружбу полученные пользователем.

    Args:
        recipient (CustomUser): Пользователь, получивший запросы.

    Returns:
        QuerySet[FriendshipRequest]: Запросы на дружбу.
    """
    return FriendshipRequest.objects.filter(to_user=recipient).select_related(
        "from_user",
        "to_user",
    )


def get_friendship(
    user1: CustomUser,
    user2: CustomUser,
) -> Optional[Friendship]:
    """
    Возвращает дружбу между двумя пользователями.

    Args:
        user1 (CustomUser): Первый пользователь.
        user2 (CustomUser): Второй пользователь.

    Returns:
        Optional[Friendship]: Дружба или None.
    """
    user1, user2 = sort_models([user1, user2])

    return Friendship.objects.filter(user1=user1, user2=user2).first()
