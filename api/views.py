from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from .models import Menu, MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


@login_required
def coffee_order(request):
    pass


@login_required
def stock_order(request):
    pass
