from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers


class UserType(models.TextChoices):
    MEMBER = ('member', '일반멤버')
    BARISTA = ('barista', '바리스타')


class User(AbstractUser):
    user_type = models.CharField(max_length=30, choices=UserType.choices, default=UserType.MEMBER, verbose_name='유저타입')
    coffee_point = models.IntegerField(default=10000)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")

    class Meta:
        model = User
        fields = ('url', 'username', 'user_type', 'coffee_point')
