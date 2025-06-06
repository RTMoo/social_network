from django.urls import path
from likes.views import like_object_view


urlpatterns = [
    path(
        route="toggle/",
        view=like_object_view,
        name="create_like_view",
    ),
]
