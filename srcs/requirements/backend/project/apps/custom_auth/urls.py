from django.urls import path
from . import views
from .views import UserCreateView

urlpatterns = [
    path('login/',  UserCreateView.as_view(), name='get'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    # path('users/signup/', views.signup, name='signup'),
    # path('users/<uuid:pk>', views.user_detail, name='user_detail'),
    # path('api/signup/', views.signup, name='signup'),
    # path('api/users/signup/', UserCreateView.as_view(), name='signup'),
    # path('api/users/', UserCreateView.as_view(), name='create-user'),
]
