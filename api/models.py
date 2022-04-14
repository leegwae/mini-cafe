from django.db import models
from rest_framework import serializers


class MenuType(models.TextChoices):
    COFFEE = ('coffee', '커피')


class Menu(models.Model):
    name = models.CharField(max_length=30, unique=True, choices=MenuType.choices, default=MenuType.COFFEE, verbose_name='메뉴')
    stock = models.IntegerField(default=20)


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ('url', 'name', 'stock')
