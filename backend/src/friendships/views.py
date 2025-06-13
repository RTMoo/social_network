from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from friendships import services


class FriendshipRequestView(APIView):
    class FriendshipRequestInputSerializer(serializers.Serializer):
        to_user = serializers.CharField()

    class FriendshipRequestOutputSerializer(serializers.Serializer):
        from_user = serializers.CharField(source="from_user.username")
        to_user = serializers.CharField(source="to_user.username")
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FriendshipRequestInputSerializer,
        responses=FriendshipRequestOutputSerializer,
    )
    def post(self, request):
        serializer = self.FriendshipRequestInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_data = services.create_friendship_request(
            from_user=request.user,
            data=serializer.validated_data,
        )
        data = self.FriendshipRequestOutputSerializer(instance=created_data).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class FriendshipRequestAcceptView(APIView):
    class FriendshipAcceptInputSerializer(serializers.Serializer):
        from_user = serializers.CharField()

    class FriendshipAcceptOutputSerializer(serializers.Serializer):
        user1 = serializers.CharField()
        user2 = serializers.CharField()
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    def get_input_serializer(self, *args, **kwargs):
        return self.FriendshipAcceptInputSerializer(*args, **kwargs)

    def get_output_serializer(self, *args, **kwargs):
        return self.FriendshipAcceptOutputSerializer(*args, **kwargs)

    @extend_schema(
        request=FriendshipAcceptInputSerializer,
        responses=FriendshipAcceptOutputSerializer,
    )
    def post(self, request):
        serializer = self.get_input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        friendship = services.accept_friendship_request(
            to_user=request.user, data=serializer.validated_data
        )
        data = self.get_output_serializer(instance=friendship).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class FriendshipRequestRejectView(APIView):
    permission_classes = [IsAuthenticated]

    class FriendshipRejectInputSerializer(serializers.Serializer):
        to_user = serializers.CharField()

    def get_input_serializer(self, *args, **kwargs):
        return self.FriendshipRejectInputSerializer(*args, **kwargs)

    @extend_schema(
        request=FriendshipRejectInputSerializer,
    )
    def post(self, request):
        serializer = self.get_input_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.reject_friendship_request(
            from_user=request.user, data=serializer.validated_data
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
