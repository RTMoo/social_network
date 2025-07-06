from django.urls import path
from chats import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:chat_id>/", consumers.ChatConsumer.as_asgi()),
]
