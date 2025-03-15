from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from project.apps.intra_oauth.views import (
    SignInIntra,
    SignInIntraCallback,
)
from project.apps.oauth.views import (
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
    # standard oauth
    path("api/signup/", SignUp.as_view(), name="signup"),
    path("api/otp/", GetOTP.as_view(), name="otp"),
    path("api/signin/", SignIn.as_view(), name="signin"),
    path("api/signout/", SignOut.as_view(), name="signout"),
    path("api/refresh_tokens/", RefreshTokens.as_view(), name="refresh_tokens"),
    # intra oauth
    path("api/signin_intra/", SignInIntra.as_view(), name="signin_intra"),
    path(
        "api/signin_intra/callback/",
        SignInIntraCallback.as_view(),
        name="signin_intra_callback",
    ),
    # users app
    path("api/users/", include("project.apps.users.urls")),
    path("api/tournaments/", include("project.apps.tournaments.urls")),
]
