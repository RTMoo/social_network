from django.urls import path
from friendships.views import (
    FriendshipRequestView,
)

urlpatterns = [
    path(
        route="requests/",
        view=FriendshipRequestView.as_view(),
        name="friendship_request",
    ),
]
