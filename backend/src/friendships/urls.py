from django.urls import path
from friendships.views import (
    FriendshipRequestAcceptView,
    FriendshipRequestSendView,
    FriendshipRequestRejectView,
    FriendshipListView,
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
]
