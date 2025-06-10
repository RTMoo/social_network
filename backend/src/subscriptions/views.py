from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from subscriptions.services import subscribe, unsubscribe


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, username: str):
        subscribe(sender=request.user, username=username)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, username: str):
        unsubscribe(sender=request.user, username=username)

        return Response(status=status.HTTP_204_NO_CONTENT)
