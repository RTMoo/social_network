from django.urls import path
from subscriptions.views import SubscribeView

urlpatterns = [
    path("subscribe/<str:username>/", SubscribeView.as_view(), name="subscribe"),
]
