from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api.models import menu, order


def index(request):
    try:
        coffee_stock = menu.Menu.objects.get(name=menu.MenuType.COFFEE).stock
    except menu.Menu.DoesNotExist:
        coffee_stock = 0
    total_order = order.Order.objects.count()
    context = {
        'coffee_stock': coffee_stock,
        'total_order': total_order
    }
    return render(request, 'index.html', context)


@login_required
def bot(request):
    menus = list(menu.Menu.objects.all())
    menu_name = [m.get_name_display() for m in menus]
    return render(request, 'bot.html', {'menus':menu_name})
