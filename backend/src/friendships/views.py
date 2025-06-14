from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from friendships import services
from friendships import selectors


class FriendshipRequestSendView(APIView):
    """
    Класс для отправки запроса на дружбу.
    """

    class FriendshipRequestOutputSerializer(serializers.Serializer):
        """
        Сериализатор для вывода данных созданного запроса на дружбу.
        """

        from_user = serializers.CharField(source="from_user.username")
        to_user = serializers.CharField(source="to_user.username")
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=FriendshipRequestOutputSerializer,
        summary="Отправить запрос на дружбу",
        description="Отправляет запрос на дружбу пользователю с указанным username.",
    )
    def post(self, request: Request, username: str):
        created_data = services.send_friendship_request(
            current_user=request.user,
            username=username,
        )

        data = self.FriendshipRequestOutputSerializer(instance=created_data).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class FriendshipRequestAcceptView(APIView):
    """
    Класс для подтверждения запроса на дружбу.
    """

    class FriendshipAcceptOutputSerializer(serializers.Serializer):
        """
        Сериализатор для вывода данных созданной дружбы.
        """

        user1 = serializers.CharField()
        user2 = serializers.CharField()
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=FriendshipAcceptOutputSerializer,
        summary="Подтвердить запрос на дружбу",
        description="Подтверждает запрос на дружбу от пользователя с указанным username.",
    )
    def post(self, request: Request, username: str):
        friendship = services.accept_friendship_request(
            to_user=request.user,
            username=username,
        )
        data = self.FriendshipAcceptOutputSerializer(instance=friendship).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class FriendshipRequestRejectView(APIView):
    """
    Класс для отклонения запроса на дружбу.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
        summary="Отклонить запрос на дружбу",
        description="Отклоняет запрос на дружбу от пользователя с указанным username.",
    )
    def delete(self, request: Request, username: str):
        services.reject_friendship_request(
            current_user=request.user,
            username=username,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendshipListView(APIView):
    """
    Класс для получения списка друзей.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=list[str],
        summary="Получить список друзей",
        description="Возвращает список друзей.",
    )
    def get(self, request: Request, username: str):
        friendships = selectors.get_friendships(username=username)

        return Response(data=friendships, status=status.HTTP_200_OK)
