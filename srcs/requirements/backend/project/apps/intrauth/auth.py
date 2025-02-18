from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class IntraAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> User:
        user_found = User.objects.filter(id=user['id'])
        if len(user_found) == 0:
            print("Creating new User")
            new_user = User.objects.create_new_intra_user(user)
            print(new_user)
            return new_user
        return user_found
        # return list(user_found).pop()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None