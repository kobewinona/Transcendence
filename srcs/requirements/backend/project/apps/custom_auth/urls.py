from django.urls import path
from . import views
from .views import UserCreateView, LoginView, LogoutView, AuthStatusView
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('login/',  LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('auth-status/', AuthStatusView.as_view(), name='auth-status'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    

    path('', RedirectView.as_view(url='login/')),
    # path('users/signup/', views.signup, name='signup'),
    # path('users/<uuid:pk>', views.user_detail, name='user_detail'),
    # path('api/signup/', views.signup, name='signup'),
    # path('api/users/signup/', UserCreateView.as_view(), name='signup'),
    # path('api/users/', UserCreateView.as_view(), name='create-user'),
]
