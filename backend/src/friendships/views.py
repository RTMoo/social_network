from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from friendships import services


class FriendshipRequestView(APIView):
    class FriendshipRequestOutputSerializer(serializers.Serializer):
        from_user = serializers.CharField(source="from_user.username")
        to_user = serializers.CharField(source="to_user.username")
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=FriendshipRequestOutputSerializer,
    )
    def post(self, request: Request, username: str):
        created_data = services.send_friendship_request(
            current_user=request.user,
            username=username,
        )

        data = self.FriendshipRequestOutputSerializer(instance=created_data).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class FriendshipRequestAcceptView(APIView):
    class FriendshipAcceptOutputSerializer(serializers.Serializer):
        user1 = serializers.CharField()
        user2 = serializers.CharField()
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=FriendshipAcceptOutputSerializer,
    )
    def post(self, request: Request, username: str):
        friendship = services.accept_friendship_request(
            to_user=request.user,
            username=username,
        )
        data = self.FriendshipAcceptOutputSerializer(instance=friendship).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class FriendshipRequestRejectView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request: Request, username: str):
        services.reject_friendship_request(
            current_user=request.user,
            username=username,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
