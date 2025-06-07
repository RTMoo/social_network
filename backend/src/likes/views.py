from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from likes.serializers import LikeSerializer
from likes.services import like_object
from likes.selectors import get_user_likes_by_type
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer


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


@extend_schema(
    responses=PostSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_post_likes_view(request: Request, username: str):
    liked_posts = get_user_likes_by_type(username=username, type="post")

    data = PostSerializer(instance=liked_posts, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    responses=CommentSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_comment_likes_view(request: Request, username: str):
    liked_comments = get_user_likes_by_type(username=username, type="comment")

    data = CommentSerializer(instance=liked_comments, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)
