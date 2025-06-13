from django.urls import path
from friendships.views import (
    FriendshipRequestAcceptView,
    FriendshipRequestView,
    FriendshipRequestRejectView,
)

urlpatterns = [
    path(
        route="requests/send/",
        view=FriendshipRequestView.as_view(),
        name="send_friendship_request",
    ),
    path(
        route="requests/accept/",
        view=FriendshipRequestAcceptView.as_view(),
        name="accept_friendship_request",
    ),
    path(
        route="requests/reject/",
        view=FriendshipRequestRejectView.as_view(),
        name="reject_friendship_request",
    ),
]
