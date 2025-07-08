from chats.models import Chat, Message
from accounts.models import CustomUser
from django.db.models import Q, Prefetch


def get_user_chats(sender: CustomUser):
    chats = (
        Chat.objects.filter(Q(user1=sender) | Q(user2=sender))
        .select_related("user1", "user2")
        .prefetch_related(
            Prefetch(
                "messages",
                queryset=Message.objects.select_related("author").order_by(
                    "-created_at"
                )[:1],
                to_attr="last_message_list",
            )
        )
    )

    for chat in chats:
        if sender == chat.user1:
            chat.second_user = chat.user2
        else:
            chat.second_user = chat.user1

        chat.last_message = (
            chat.last_message_list[-1] if chat.last_message_list else None
        )

    return chats


def get_chat_messages(chat_id: int):
    messages = Message.objects.filter(chat_id=chat_id).select_related("author")

    return messages
