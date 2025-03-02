from django.http import HttpResponse
from django.contrib import admin
from django.urls import path


# Rest Framework
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from project.apps.custom_auth.views import UserCreateView, GetOTPView, VerifyOTPView, AuthStatusView, ProfileViewSet

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


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    
     # Custom auth endpoints
    path('api/signup/', UserCreateView.as_view(), name='signup'),
    path('api/auth-status/', AuthStatusView.as_view(), name='auth-status'),
    path('api/token/', permission_classes([AllowAny])(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', permission_classes([AllowAny])(TokenRefreshView.as_view()), name='token_refresh'),   
    path('api/get-otp/', GetOTPView.as_view(), name='get_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
