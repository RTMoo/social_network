from typing import Any
from uuid import uuid4
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from profiles.selectors import get_profile
from profiles.models import Profile
from profiles.utils import make_circle_avatar
from accounts.models import CustomUser


def create_profile(user: CustomUser) -> None:
    Profile.objects.create(user=user)


def update_profile(request: Request, username: str, data: dict[str, Any]) -> Profile:
    profile = get_profile(username)

    if request.user.username != username:
        raise PermissionDenied(detail="Вы не можете изменить чужой профиль.")

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
