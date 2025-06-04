from rest_framework.exceptions import NotFound
from profiles.models import Profile


def get_profile(username: str) -> Profile:
    profile = Profile.objects.filter(user__username=username).first()

    if not profile:
        raise NotFound(detail="Профиль не найдено.")

    return profile
