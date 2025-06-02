from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from posts.serializers import PostSerializer
from posts.services import create_post, update_post, delete_post
from posts.selectors import get_user_posts, get_post


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


@extend_schema(
    responses=PostSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_posts_view(request: Request, username: str):
    posts = get_user_posts(username=username)

    data = PostSerializer(instance=posts, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    responses=PostSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_post_view(request: Request, post_id: int):
    post = get_post(post_id=post_id)

    data = PostSerializer(instance=post).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    responses=PostSerializer,
    request=PostSerializer,
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_post_view(request: Request, post_id: int):
    serializer = PostSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    updated_post = update_post(data=serializer.validated_data, post_id=post_id)

    data = PostSerializer(instance=updated_post).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post_view(request: Request, post_id: int):
    delete_post(post_id=post_id, author=request.user)

    return Response(status=status.HTTP_204_NO_CONTENT)
