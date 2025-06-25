from accounts.models import CustomUser
from rest_framework.exceptions import NotFound


def get_user(username: str) -> CustomUser:
    """
    Возвращает пользователя по username.

    Args:
        username (str): Имя пользователя.

    Returns:
        CustomUser: Объект пользователя.

    Raises:
        NotFound: Если пользователь не найден.
    """
    user = CustomUser.objects.filter(username=username).first()

    if not user:
        raise NotFound(detail="Пользователь не найден.")

    return user
