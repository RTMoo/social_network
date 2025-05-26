from django.conf import settings


def set_jwt_token(response, access_token: str, refresh_token: str = None):
    """
    Установка куки к ответу
    """

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE", False),
        samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE", "Lax"),
        max_age=settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds(),
    )

    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE", False),
            samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE", "Lax"),
            max_age=settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME").total_seconds(),
        )

    return response
