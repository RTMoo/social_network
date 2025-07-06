from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from chats.serializers import CreateChatSerializer, ChatSerializer, MessageSerializer
from chats.services import create_chat
from chats.selectors import get_user_chats, get_chat_messages


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_chat_view(request: Request):
    serializer = CreateChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    from_user = request.user
    to_user = serializer.validated_data["to_user"]

    created_chat = create_chat(user1=from_user, user2_username=to_user)
    data = ChatSerializer(instance=created_chat).data

    return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chat_list_view(request: Request):
    user_chats = get_user_chats(sender=request.user)
    data = ChatSerializer(instance=user_chats, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chat_messages_view(request: Request, chat_id: int):
    chat_messages = get_chat_messages(chat_id=chat_id)
    data = MessageSerializer(instance=chat_messages, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)
