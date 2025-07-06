import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import Chat, Message
from accounts.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id: int = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name: str = f"chat_{self.chat_id}"
        self.user: CustomUser = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text = json.loads(text_data)["text"]

        message = await self.create_message(
            chat_id=self.chat_id,
            sender=self.user,
            text=text,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": {
                    "id": message.id,
                    "sender": self.user.username,
                    "text": message.text,
                    "created_at": str(message.created_at),
                },
            },
        )

    @database_sync_to_async
    def create_message(self, chat_id: int, sender: CustomUser, text: str):
        chat = Chat.objects.filter(id=chat_id).first()
        message = Message.objects.create(chat=chat, author=sender, text=text)

        return message

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
