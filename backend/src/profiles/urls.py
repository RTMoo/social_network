from django.urls import path
from profiles.views import get_profile_view


urlpatterns = [
    path(route="<str:username>/", view=get_profile_view, name="get_pofile"),
]
