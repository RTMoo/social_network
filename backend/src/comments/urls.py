from django.urls import path
from comments.views import create_comment_view

urlpatterns = [
    path(route="create/", view=create_comment_view, name="create_comment"),
]
