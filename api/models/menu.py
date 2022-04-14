from django.db import models
from rest_framework import serializers


class MenuType(models.TextChoices):
    COFFEE = ('coffee', '커피')


class Menu(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            choices=MenuType.choices, default=MenuType.COFFEE)
    price = models.PositiveIntegerField(default=3000)
    stock = models.PositiveIntegerField(default=20)

    class Meta:
        ordering = ['-stock']

    def __str__(self):
        return self.name


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ('url', 'name', 'price', 'stock')
