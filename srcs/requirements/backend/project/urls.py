from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from project.apps.intrauth.views import home, intra_login, intra_login_redirect, get_authenticated_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from project.apps.custom_auth.views import UserCreateView, GetOTPView, VerifyOTPView, AuthStatusView

# Import settings and static helper for serving static files during development
from django.conf import settings
from django.conf.urls.static import static

""" 
    don’t need to define each URL pattern manually.
    Only register views with the router, which 
    then automatically generates the necessary CRUD routes.
    for profile

"""
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='login/')),
    #intra oauth
    path('auth/user/', get_authenticated_user, name='get_authenticated_user'),
    path('oauth/', home, name='oauth'),
    path('oauth/login/', intra_login, name='oauth_login'),
    path('oauth/redirect/', intra_login_redirect, name='oauth_login_redirect'),
    
    # Custom auth endpoints
    path('api/signup/', UserCreateView.as_view(), name='signup'),
    path('api/auth-status/', AuthStatusView.as_view(), name='auth-status'),
    path('api/token/', permission_classes([AllowAny])(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', permission_classes([AllowAny])(TokenRefreshView.as_view()), name='token_refresh'),   
    path('api/get-otp/', GetOTPView.as_view(), name='get_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]