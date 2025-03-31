from typing import List, Union

from django.urls import URLPattern, URLResolver
from django.urls import path
from project.apps.tournaments.views import UserTournaments

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("", UserTournaments.as_view(), name="user_tournaments"),
    path(
        "<uuid:tournament_id>",
        UserTournaments.as_view(),
        name="update_tournament_result",
    ),
]
