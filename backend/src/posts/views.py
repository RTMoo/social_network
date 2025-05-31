from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from posts.serializers import PostSerializer
from posts.services import create_post


@extend_schema(
    request=PostSerializer,
    responses=PostSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post_view(request: Request):
    serializer = PostSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    created_post = create_post(serializer.validated_data, author=request.user)
    data = PostSerializer(instance=created_post).data

    return Response(data=data, status=status.HTTP_201_CREATED)
