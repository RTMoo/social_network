from typing import Any
from uuid import uuid4
from rest_framework.request import Request
from profiles.selectors import get_profile
from profiles.models import Profile
from profiles.utils import make_circle_avatar
from accounts.models import CustomUser


def create_profile(user: CustomUser) -> None:
    Profile.objects.create(user=user)


def update_profile(request: Request, data: dict[str, Any]) -> Profile:
    profile = get_profile(user_id=request.user.id)

    for key, value in data.items():
        if key == "avatar" and value:
            # Обработка аватарки
            processed = make_circle_avatar(value)
            filename = f"{uuid4()}.png"
            profile.avatar.save(filename, processed, save=False)
        else:
            setattr(profile, key, value)

    profile.save()
    return profile
