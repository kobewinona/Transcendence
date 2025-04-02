from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from project.apps.oauth.views import (
    SignUp,
    GetOTP,
    SignIn,
    RefreshTokens,
    SignInIntra,
    SignInIntraCallback,
    SignOut,
)


def home(request):
    return HttpResponse("Hello, Django is running!")


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    # oauth
    path("api/signup/", SignUp.as_view(), name="signup"),
    path("api/otp/", GetOTP.as_view(), name="otp"),
    path("api/signin/", SignIn.as_view(), name="signin"),
    path("api/signout/", SignOut.as_view(), name="signout"),
    path("api/refresh_tokens/", RefreshTokens.as_view(), name="refresh_tokens"),
    path("api/signin_intra/", SignInIntra.as_view(), name="signin_intra"),
    path(
        "api/signin_intra/callback/",
        SignInIntraCallback.as_view(),
        name="intra_signin_callback",
    ),
    # users
    path("api/users/", include("project.apps.users.urls")),
    path("api/tournaments/", include("project.apps.tournaments.urls")),
]
