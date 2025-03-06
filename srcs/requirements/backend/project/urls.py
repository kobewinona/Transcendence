from django.http import HttpResponse
from django.contrib import admin
from django.urls import path


# Rest Framework
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from project.apps.custom_auth.views import UserCreateView, GetOTPView, VerifyOTPView, AuthStatusView
from project.apps.intrauth.views import home, intra_login, intra_login_redirect, get_authenticated_user


""" 
    don’t need to define each URL pattern manually.
    Only register views with the router, which 
    then automatically generates the necessary CRUD routes.
    for profile
    so for profile view  it will be 
    GET /profiles/ -> List all profiles
    POST /profiles/ -> Create a new profile.
    GET /profiles/<id>/ -> Retrieve a specific profile.
    PUT /profiles/<id>/ ->Update a specific profile.
    DELETE /profiles/<id>/ ->Delete a specific profile.
    for vue ot will be (/api/profiles/) using a GET
"""
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'profiles', ProfileViewSet)


def home(request):
    return HttpResponse("Hello, Django is running!")
def intra_api(request):
    return HttpResponse("Wow, its working everywhere!")


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    
    path('auth/user/', get_authenticated_user, name='get_authenticated_user'),
    path('oauth/intra', intra_api, name='intra'),
    path('oauth/login/', intra_login, name='oauth_login'),
    path('oauth/redirect/', intra_login_redirect, name='oauth_login_redirect'),
    
     # Custom auth endpoints
    path('api/signup/', UserCreateView.as_view(), name='signup'),
    path('api/auth-status/', AuthStatusView.as_view(), name='auth-status'),
    
    path('api/get-otp/', GetOTPView.as_view(), name='get_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    
    # JWT token endpoints
    path('api/token/', permission_classes([AllowAny])(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', permission_classes([AllowAny])(TokenRefreshView.as_view()), name='token_refresh'),   
]
