from rest_framework.exceptions import NotFound
from profiles.models import Profile
from accounts.models import CustomUser
from subscriptions.selectors import subscribe_exists

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

    profile.is_subscribed = subscribe_exists(sender=sender, username=username)

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
