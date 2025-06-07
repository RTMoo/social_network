from django.urls import path
from likes.views import (
    like_comment_view,
    like_post_view,
    get_user_liked_comments_view,
    get_user_liked_posts_view,
)


urlpatterns = [
    path(
        route="post/<int:post_id>/",
        view=like_post_view,
        name="like_post",
    ),
    path(
        route="comment/<int:comment_id>/",
        view=like_comment_view,
        name="like_comment",
    ),
    path(
        route="users/<str:username>/posts/",
        view=get_user_liked_posts_view,
        name="get_user_post_likes",
    ),
    path(
        route="users/<str:username>/comments/",
        view=get_user_liked_comments_view,
        name="get_user_comment_likes",
    ),
]
