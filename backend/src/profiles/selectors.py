from rest_framework.exceptions import NotFound
from profiles.models import Profile
from accounts.models import CustomUser


def get_profile(username: str) -> Profile:
    profile = (
        Profile.objects.filter(user__username=username).select_related("user").first()
    )

    if not profile:
        raise NotFound(detail="Профиль не найдено.")

    return profile


def get_my_profile(user: CustomUser) -> Profile:
    profile = Profile.objects.filter(user=user).select_related("user").first()

    if not profile:
        raise NotFound(detail="Профиль не найдено.")

    return profile
