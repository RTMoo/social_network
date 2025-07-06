from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_chat_list_view, name="get_chat_list"),
    path("create/", views.create_chat_view, name="create_chat"),
    path("<int:chat_id>/messages/", views.get_chat_messages_view, name="chat_messages"),
]
