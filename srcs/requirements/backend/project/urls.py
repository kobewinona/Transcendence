from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from project.apps.custom_auth.views import (
    SignUp,
    GetOTP,
    SignIn,
    RefreshTokens,
    SignOut,
)


def home(request):
    return HttpResponse("Hello, Django is running!")


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/signup/", SignUp.as_view(), name="signup"),
    path("api/otp/", GetOTP.as_view(), name="otp"),
    path("api/signin/", SignIn.as_view(), name="signin"),
    path("api/signout/", SignOut.as_view(), name="signout"),
    path("api/refresh_tokens/", RefreshTokens.as_view(), name="refresh_tokens"),
    path("api/users/", include("project.apps.users.urls")),
]
