from django.urls import path
from likes.views import like_object_view, get_user_post_likes_view, get_user_comment_likes_view


urlpatterns = [
    path(
        route="toggle/",
        view=like_object_view,
        name="create_like_view",
    ),
    path(
        route="<str:username>/posts/",
        view=get_user_post_likes_view,
        name="get_user_post_likes",
    ),
    path(
        route="<str:username>/comments/",
        view=get_user_comment_likes_view,
        name="get_user_comment_likes",
    ),
]
