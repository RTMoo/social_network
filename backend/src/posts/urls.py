from django.urls import path
from posts.views import create_post_view


urlpatterns = [
    path(route="create/", view=create_post_view, name="create_post"),
]
