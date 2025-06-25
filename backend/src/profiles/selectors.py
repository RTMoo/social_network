from rest_framework.exceptions import NotFound
from profiles.models import Profile
from accounts.models import CustomUser


def get_profile(username: str) -> Profile:
    """
    Возвращает профиль пользователя по username.

    Args:
        username (str): username пользователя.

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
