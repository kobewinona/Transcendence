from django.urls import path
from . import views
from .views import UserCreateView, LoginView, LogoutView, AuthStatusView
from django.views.generic import RedirectView

urlpatterns = [
    path('login/',  LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('auth-status/', AuthStatusView.as_view(), name='auth-status'),
    path('', RedirectView.as_view(url='login/')),
    # path('users/signup/', views.signup, name='signup'),
    # path('users/<uuid:pk>', views.user_detail, name='user_detail'),
    # path('api/signup/', views.signup, name='signup'),
    # path('api/users/signup/', UserCreateView.as_view(), name='signup'),
    # path('api/users/', UserCreateView.as_view(), name='create-user'),
]
