from channels.routing import ProtocolTypeRouter, URLRouter
from chats.routing import websocket_urlpatterns
from chats.middleware import JWTAuthMiddleware
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
