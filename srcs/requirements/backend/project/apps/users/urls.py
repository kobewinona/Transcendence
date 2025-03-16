from typing import List, Union

from django.urls import path, URLPattern, URLResolver
from project.apps.users.views import UserInfo

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("me/", UserInfo.as_view(), name="user_info"),
]
