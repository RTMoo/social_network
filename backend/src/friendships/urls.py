from django.urls import path
from friendships.views import (
    FriendshipRequestAcceptView,
    FriendshipRequestSendView,
    FriendshipRequestRejectView,
    FriendshipListView,
    FriendshipReceivedRequestListView,
    FriendshipSentRequestListView,
)

urlpatterns = [
    path(
        route="requests/<str:username>/send/",
        view=FriendshipRequestSendView.as_view(),
        name="send_friendship_request",
    ),
    path(
        route="requests/<str:username>/accept/",
        view=FriendshipRequestAcceptView.as_view(),
        name="accept_friendship_request",
    ),
    path(
        route="requests/<str:username>/reject/",
        view=FriendshipRequestRejectView.as_view(),
        name="reject_friendship_request",
    ),
    path(
        route="<str:username>/list/",
        view=FriendshipListView.as_view(),
        name="friendship_list",
    ),
    path(
        route="requests/received/",
        view=FriendshipReceivedRequestListView.as_view(),
        name="friendship_received_request_list",
    ),
    path(
        route="requests/sent/",
        view=FriendshipSentRequestListView.as_view(),
        name="friendship_sent_request_list",
    ),
]
