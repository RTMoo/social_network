from django.urls import path
from posts.views import (
    create_post_view,
    get_user_posts_view,
    get_post_view,
    update_post_view,
    delete_post_view,
    get_subscribtion_posts_view,
)


urlpatterns = [
    path(
        route="create/",
        view=create_post_view,
        name="create_post",
    ),
    path(
        route="list/<str:username>/",
        view=get_user_posts_view,
        name="get_user_posts",
    ),
    path(
        route="get/<int:post_id>/",
        view=get_post_view,
        name="get_post",
    ),
    path(
        route="update/<int:post_id>/",
        view=update_post_view,
        name="update_post",
    ),
    path(
        route="delete/<int:post_id>/",
        view=delete_post_view,
        name="delete_post",
    ),
    path(
        route="subscriptions_posts/",
        view=get_subscribtion_posts_view,
        name="subscriptions_posts",
    ),
]
