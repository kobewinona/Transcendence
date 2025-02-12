from django.contrib.auth import models

class IntraUserManager(models.UserManager):
    def create_new_intra_user(self, user):
        print("inside creating new user")
        new_user = self.create(
            id=user['id'],
            intra_login=user['login'],
            email=user.get('email'),
            avatar=user.get('image_url', '')
        )
        # new_user.save()  # Explicitly save user
        # print("New user created:", new_user)
        return new_user