from chats.models import Chat, Message
from accounts.models import CustomUser
from accounts.selectors import get_user
from friendships.utils import sort_models


def create_chat(user1: CustomUser, user2_username: str) -> Chat:
    user2 = get_user(username=user2_username)

    user1, user2 = sort_models([user1, user2])

    chat = Chat.objects.filter(user1=user1, user2=user2).first()
    if not chat:
        chat = Chat.objects.create(user1=user1, user2=user2)

    chat.second_user = user2
    chat.last_message = Message.objects.filter(chat_id=chat.id).last()
    return chat
