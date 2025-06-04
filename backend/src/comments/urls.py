from django.urls import path
from comments.views import (
    create_comment_view,
    get_post_comments_view,
    get_comment_replies_view,
)

urlpatterns = [
    path(
        route="create/",
        view=create_comment_view,
        name="create_comment",
    ),
    path(
        route="post/<int:post_id>/",
        view=get_post_comments_view,
        name="get_post_comments",
    ),
    path(
        route="<int:comment_id>/",
        view=get_comment_replies_view,
        name="get_comment_replies",
    ),
]
