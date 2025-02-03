from django.contrib.auth import models

class IntraUserManager(models.UserManager):
    def create_new_intra_user(self, user):
        new_user = self.create(
            id=user['id'],
            intra_login=user['login'],
            wallet=user['wallet'],
        )
        new_user.create_associated_players(self)
        return new_user