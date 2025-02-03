from django.contrib.auth.backends import BaseBackend
from .models import IntraUser

class IntraAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> IntraUser:
        user_found = IntraUser.objects.filter(id=user['id'])
        if len(user_found) == 0:
            print("Creating new IntraUser", flush=True)
            new_user = IntraUser.objects.create_new_intra_user(user)
            return new_user
        return list(user_found).pop()

    def get_user(self, user_id):
        try:
            return IntraUser.objects.get(pk=user_id)
        except IntraUser.DoesNotExist:
            return None