from django.urls import path
from subscriptions.views import (
    SubscribeView,
    SubscriptionsListView,
    SubscribersListView,
)

urlpatterns = [
    path(
        "subscribe/<str:username>/",
        SubscribeView.as_view(),
        name="subscribe",
    ),
    path(
        "<str:username>/subscription-list/",
        SubscriptionsListView.as_view(),
        name="subscriptions",
    ),
    path(
        "<str:username>/subscriber-list/",
        SubscribersListView.as_view(),
        name="subscribers",
    ),
]
