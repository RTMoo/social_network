from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from friendships.services import create_friendship_request, create_friendship


class FriendshipRequestView(APIView):
    class FriendshipRequestInputSerializer(serializers.Serializer):
        to_user = serializers.CharField()

    class FriendshipRequestOutputSerializer(serializers.Serializer):
        from_user = serializers.CharField()
        to_user = serializers.CharField()
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FriendshipRequestInputSerializer,
        responses=FriendshipRequestOutputSerializer,
    )
    def post(self, request):
        serializer = self.FriendshipRequestInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_data = create_friendship_request(
            from_user=request.user,
            data=serializer.validated_data,
        )
        data = self.FriendshipRequestOutputSerializer(instance=created_data).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class FriendshipView(APIView):
    class FriendshipInputSerializer(serializers.Serializer):
        from_user = serializers.CharField()

    class FriendshipOutputSerializer(serializers.Serializer):
        user1 = serializers.CharField()
        user2 = serializers.CharField()
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FriendshipInputSerializer,
        responses=FriendshipOutputSerializer,
    )
    def post(self, request):
        serializer = self.FriendshipInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        friendship = create_friendship(
            to_user=request.user, data=serializer.validated_data
        )
        data = self.FriendshipOutputSerializer(instance=friendship).data

        return Response(data=data, status=status.HTTP_201_CREATED)
