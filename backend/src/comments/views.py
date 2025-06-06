from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from comments.services import create_comment, update_comment, delete_comment
from comments.selectors import get_post_comments, get_comment_replies, get_user_comments
from comments.serializers import CommentSerializer, CommentUpdateSerializer
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


@extend_schema(
    responses=CommentSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_post_comments_view(request: Request, post_id: int):
    comments = get_post_comments(post_id=post_id)

    data = CommentSerializer(instance=comments, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    responses=CommentSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_comment_replies_view(request: Request, comment_id: int):
    replies = get_comment_replies(comment_id=comment_id)

    data = CommentSerializer(instance=replies, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    responses=CommentSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_comments_view(request: Request, username: str):
    comments = get_user_comments(username=username)

    data = CommentSerializer(instance=comments, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    request=CommentUpdateSerializer,
    responses=CommentSerializer,
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_comment_view(request: Request, comment_id: int):
    serializer = CommentUpdateSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    updated_comment = update_comment(
        data=serializer.validated_data,
        comment_id=comment_id,
        sender=request.user,
    )

    data = CommentSerializer(instance=updated_comment).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment_view(request: Request, comment_id: int):
    delete_comment(comment_id=comment_id, sender=request.user)

    return Response(status=status.HTTP_204_NO_CONTENT)
