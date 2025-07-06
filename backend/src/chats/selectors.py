from chats.models import Chat, Message
from accounts.models import CustomUser
from django.db.models import Q


def get_user_chats(sender: CustomUser):
    chats = (
        Chat.objects.filter(
            Q(user1=sender) | Q(user2=sender),
        )
        .select_related("user1", "user2")
        .prefetch_related("messages")
    )

    for chat in chats:
        if sender == chat.user1:
            chat.second_user = chat.user2
        else:
            chat.second_user = chat.user1

        chat.last_message = chat.messages.last()

    return chats


def get_chat_messages(chat_id: int):
    messages = Message.objects.filter(chat_id=chat_id).select_related("author")

    return messages
