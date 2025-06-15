from django.urls import path
from friendships import views


urlpatterns = [
    path(
        route="requests/<str:username>/send/",
        view=views.FriendshipRequestSendView.as_view(),
        name="send_friendship_request",
    ),
    path(
        route="requests/<str:username>/accept/",
        view=views.FriendshipRequestAcceptView.as_view(),
        name="accept_friendship_request",
    ),
    path(
        route="requests/<str:username>/reject/",
        view=views.FriendshipRequestRejectView.as_view(),
        name="reject_friendship_request",
    ),
    path(
        route="<str:username>/list/",
        view=views.FriendshipListView.as_view(),
        name="friendship_list",
    ),
    path(
        route="requests/received/",
        view=views.FriendshipReceivedRequestListView.as_view(),
        name="friendship_received_request_list",
    ),
    path(
        route="requests/sent/",
        view=views.FriendshipSentRequestListView.as_view(),
        name="friendship_sent_request_list",
    ),
    path(
        route="<str:username>/delete/",
        view=views.FriendshipDeleteView.as_view(),
        name="delete_friendship",
    ),
]
