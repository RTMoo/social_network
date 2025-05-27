from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile_by_username


@api_view(["GET"])
@permission_classes([AllowAny])
def get_profile_view(request: Request, username: str):
    profile = get_profile_by_username(username)
    data = ProfileSerializer(instance=profile).data

    return Response(data=data)
