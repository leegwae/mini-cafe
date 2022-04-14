from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType(models.TextChoices):
    MEMBER = ('member', '일반멤버')
    BARISTA = ('barista', '바리스타')


class User(AbstractUser):
    user_type = models.CharField(max_length=30, choices=UserType.choices, default=UserType.MEMBER, verbose_name='유저타입')
