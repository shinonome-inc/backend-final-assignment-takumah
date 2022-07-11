from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models import EmailField


class User(AbstractUser, PermissionsMixin):
    email = EmailField("メールアドレス")


# class FriendShip(models.Model):
#     pass
