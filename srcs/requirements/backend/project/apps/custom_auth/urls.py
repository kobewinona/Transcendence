from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api
# from .views import get_users, create_user, user_detail

urlpatterns = [
    # path('', views.index, name='chat-index'),
    path('signup/',api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('users/', get_users, name='get_users'),
    # path('users/create/', create_user, name='create_user'),
    # path('users/<int:pk>', user_detail, name='user_detail')
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
#     path('api/login', views.login_view, name='login'),
#     path('api/logout', views.logout_view, name='logout'),
#     path('api/user', views.user, name='user'),
#     path('api/register', views.register, name='register'),
# ]
