from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from comments.services import create_comment
from comments.serializers import CommentSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    request=CommentSerializer,
    responses=CommentSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment_view(request: Request):
    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    created_comment = create_comment(serializer.validated_data, author=request.user)

    data = CommentSerializer(instance=created_comment).data

    return Response(data=data, status=status.HTTP_201_CREATED)
