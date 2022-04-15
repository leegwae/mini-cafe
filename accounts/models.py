from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType(models.TextChoices):
    MEMBER = ('member', '일반멤버')
    BARISTA = ('barista', '바리스타')


class User(AbstractUser):
    nickname = models.CharField(max_length=10, blank=False, verbose_name="닉네임")
    user_type = models.CharField(max_length=30, choices=UserType.choices, default=UserType.MEMBER, verbose_name="유저타입")
    coffee_point = models.PositiveIntegerField(default=10000)

    class Meta:
        ordering = ['-id']
