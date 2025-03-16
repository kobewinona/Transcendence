from typing import List, Union

from django.urls import URLPattern, URLResolver

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # path("me/", UserInfo.as_view(), name="user_info"),
]
