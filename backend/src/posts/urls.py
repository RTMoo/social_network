from django.urls import path
from posts.views import create_post_view, get_user_posts_view


urlpatterns = [
    path(route="create/", view=create_post_view, name="create_post"),
    path(route="<str:username>/", view=get_user_posts_view, name="get_user_posts"),
]
