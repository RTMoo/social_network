from django.urls import path
from search.views import search_profiles_view


urlpatterns = [
    path(
        route="",
        view=search_profiles_view,
        name="search_profiles",
    ),
]
