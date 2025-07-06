from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.auth = JWTAuthentication()

    @database_sync_to_async
    def get_user(self, token):
        try:
            validated_token = self.auth.get_validated_token(token)
            user = self.auth.get_user(validated_token)
            return user
        except Exception:
            return AnonymousUser()

    async def __call__(self, scope, receive, send):
        headers = dict(scope.get("headers", []))
        cookies = headers.get(b"cookie", b"").decode()

        token = None
        for cookie in cookies.split("; "):
            if cookie.startswith("access_token="):  # или имя из settings
                token = cookie.split("=")[1]

        scope["user"] = await self.get_user(token) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)
