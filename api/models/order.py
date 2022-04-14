from django.db import models
from rest_framework import serializers

from accounts.models import User
from . import menu


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    menu = models.ForeignKey(menu.Menu, on_delete=models.SET_NULL)
    count = models.PositiveIntegerField(default=1)
    is_done = models.BooleanField(default=False)

    @property
    def amount(self):
        return self.menu.price * self.count

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username + ":" + str(self.created_at)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    menu = serializers.SlugRelatedField(queryset=menu.Menu.objects.all(), slug_field='name')

    class Meta:
        model = Order
        fields = ('url', 'pk', 'user', 'menu', 'count', 'amount', 'created_at', 'is_done')
