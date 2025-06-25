from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from subscriptions.services import subscribe, unsubscribe
from subscriptions.selectors import get_user_subscriptions, get_user_subscribers
from profiles.serializers import ProfileSerializer


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, username: str):
        subscribe(sender=request.user, username=username)

        return Response(status=status.HTTP_201_CREATED)


class UnsubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, username: str):
        unsubscribe(sender=request.user, username=username)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, username: str):
        subscriptions = get_user_subscriptions(username=username)
        data = ProfileSerializer(instance=subscriptions, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)


class SubscribersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, username: str):
        subscribers = get_user_subscribers(username=username)
        data = ProfileSerializer(instance=subscribers, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)
