from rest_framework.exceptions import NotFound
from profiles.models import Profile
from accounts.models import CustomUser
from subscriptions.selectors import subscribe_exists
from friendships.selectors import friend_exists, friend_request_exists


def get_profile(username: str, sender: CustomUser) -> Profile:
    """
    Возвращает профиль пользователя по username.

    Args:
        username (str): username пользователя.
        sender (CustomUser): Пользователь, который запрашивает профиль.
    Returns:
        Profile: Профиль пользователя.

    Raises:
        NotFound: Если профиль не найден.
    """
    profile = (
        Profile.objects.filter(user__username=username).select_related("user").first()
    )

    if not profile:
        raise NotFound(detail="Профиль не найден.")

    if sender.is_authenticated:
        profile.is_subscribed = subscribe_exists(
            subscriber=sender.username,
            to_subscribe=username,
        )

        profile.is_friend = friend_exists(
            user1=sender,
            user2=profile.user,
        )

        if not profile.is_friend:
            profile.friend_request_sent = friend_request_exists(
                from_user=sender,
                to_user=profile.user,
            )

    else:
        profile.is_subscribed = False
        profile.friend_request_sent = False
        profile.is_friend = False

    return profile


def get_my_profile(user: CustomUser) -> Profile:
    """
    Возвращает профиль текущего пользователя.

    Args:
        user (CustomUser): Текущий пользователь.

    Returns:
        Profile: Профиль пользователя.

    Raises:
        NotFound: Если профиль не найден.
    """
    profile = Profile.objects.filter(user=user).select_related("user").first()

    if not profile:
        raise NotFound(detail="Профиль не найден.")

    return profile
