from django.urls import path
from subscriptions.views import (
    SubscribeView,
    SubscriptionsListView,
    SubscribersListView,
    UnsubscribeView,
    DeleteSubscriberView,
)

urlpatterns = [
    path(
        "subscribe/<str:username>/",
        SubscribeView.as_view(),
        name="subscribe",
    ),
    path(
        "unsubscribe/<str:username>/",
        UnsubscribeView.as_view(),
        name="unsubscribe",
    ),
    path(
        "delete-subscriber/<str:username>/",
        DeleteSubscriberView.as_view(),
        name="delete-subscriber",
    ),
    path(
        "subscriptions/<str:username>/",
        SubscriptionsListView.as_view(),
        name="subscriptions",
    ),
    path(
        "subscribers/<str:username>/",
        SubscribersListView.as_view(),
        name="subscribers",
    ),
]
