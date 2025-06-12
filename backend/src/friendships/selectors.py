from friendships.models import FriendshipRequest, Friendship
from rest_framework.exceptions import NotFound


def get_friendship_request(from_user, to_user) -> FriendshipRequest:
    request = FriendshipRequest.objects.filter(
        from_user=from_user, to_user=to_user
    ).first()

    if not request:
        raise NotFound(detail="Запрос дружбы не найден")

    return request


def friend_available(user1, user2) -> bool:
    user1, user2 = sorted([user1, user2], key=lambda user: user.pk)

    return Friendship.objects.filter(user1=user1, user2=user2).exists()
