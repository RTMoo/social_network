from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from likes.services import like_post, like_comment
from likes.selectors import get_user_liked_comments, get_user_liked_posts
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post_view(request: Request, post_id: int):
    liked = like_post(post_id=post_id, sender=request.user)

    return Response(data=liked, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_comment_view(request: Request, comment_id: int):
    liked = like_comment(comment_id=comment_id, sender=request.user)

    return Response(data=liked, status=status.HTTP_200_OK)


@extend_schema(
    responses=PostSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_liked_posts_view(request: Request, username: str):
    liked_posts = get_user_liked_posts(username=username)

    data = PostSerializer(instance=liked_posts, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    responses=CommentSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_liked_comments_view(request: Request, username: str):
    liked_comments = get_user_liked_comments(username=username)

    data = CommentSerializer(instance=liked_comments, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)
