from django.urls import path
from project.apps.users.views import UserInfo


urlpatterns = [
    path("me/", UserInfo.as_view(), name="user_info"),
]
