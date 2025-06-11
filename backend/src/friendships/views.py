from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from friendships.services import create_friendship_request


class FriendshipRequestView(APIView):
    class InputSerializer(serializers.Serializer):
        to_user = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        from_user = serializers.CharField()
        to_user = serializers.CharField()
        created_at = serializers.DateTimeField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=InputSerializer,
        responses=OutputSerializer,
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_data = create_friendship_request(
            from_user=request.user,
            data=serializer.validated_data,
        )
        data = self.OutputSerializer(instance=created_data).data

        return Response(data=data, status=status.HTTP_200_OK)
