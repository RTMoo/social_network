from django.urls import path
from friendships.views import (
    FriendshipRequestView,
    FriendshipView,
)

urlpatterns = [
    path(
        route="requests/",
        view=FriendshipRequestView.as_view(),
        name="friendship_request",
    ),
    path(
        route="friends/",
        view=FriendshipView.as_view(),
        name="friendship",
    ),
]
