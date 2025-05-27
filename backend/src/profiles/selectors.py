from rest_framework.exceptions import NotFound
from profiles.models import Profile


def get_profile_by_username(username: str) -> Profile:
    profile = Profile.objects.filter(user__username=username).first()

    if not profile:
        raise NotFound(detail=f"Профиль с именем '{username}' не найдено.")

    return profile
