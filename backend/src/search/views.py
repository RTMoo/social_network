from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from search.selectors import search_profiles
from profiles.serializers import ProfileSerializer
from rest_framework import status


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_profiles_view(request: Request):
    query = request.GET.get("q")

    profiles = search_profiles(query=query)
    data = ProfileSerializer(instance=profiles, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)
