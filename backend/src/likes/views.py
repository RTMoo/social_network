from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from likes.serializers import LikeSerializer
from likes.services import like_object


@extend_schema(
    request=LikeSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_object_view(request: Request):
    serializer = LikeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    like_object(data=serializer.validated_data, sender=request.user)

    return Response(status=status.HTTP_201_CREATED)
