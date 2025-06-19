from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile, get_my_profile
from profiles.services import update_profile


@api_view(["GET"])
@permission_classes([AllowAny])
def get_profile_view(request: Request, username: str):
    profile = get_profile(username)
    data = ProfileSerializer(instance=profile).data

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_profile_view(request: Request):
    profile = get_my_profile(user=request.user)
    data = ProfileSerializer(instance=profile).data

    return Response(data=data, status=status.HTTP_200_OK)


@extend_schema(
    request=ProfileSerializer,
    responses=ProfileSerializer,
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile_view(request: Request):
    serializer = ProfileSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    updated_profile = update_profile(request, serializer.validated_data)
    data = ProfileSerializer(instance=updated_profile).data

    return Response(data=data, status=status.HTTP_200_OK)
