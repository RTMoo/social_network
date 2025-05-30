from rest_framework.exceptions import NotFound
from profiles.models import Profile


def get_profile(user_id: int) -> Profile:
    profile = Profile.objects.filter(user_id=user_id).first()

    if not profile:
        raise NotFound(detail="Профиль не найдено.")

    return profile
