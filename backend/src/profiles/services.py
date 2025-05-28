from typing import Any
from profiles.selectors import get_profile


def update_profile(username: str, data: dict[str, Any]):
    profile = get_profile(username)

    for key, value in data.items():
        setattr(profile, key, value)

    profile.save()
    return profile
