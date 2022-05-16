from django.test import TransactionTestCase

from accounts.models import User, UserType
from api import tasks
from api.models import menu, order
from config.params import *


class CeleryTestCase(TransactionTestCase):

    def setUp(self):
        self.alice = User.objects.create(username="멤버1", user_type=UserType.MEMBER, coffee_point=10000)
        self.coffee = menu.Menu.objects.create(name="커피", price=3000, stock=30)

    def test_샐러리_주문_진행(self):
        # given
        order_obj = order.Order.objects.create(user=self.alice, menu=self.coffee, count=1, is_done=False)
        order_dic = order_obj.__dict__
        # when
        tasks.order_in_progress(order_dic)
        # then
        new_order_obj = order.Order.objects.get(id=order_dic['id'])
        self.assertEqual(new_order_obj.is_done, True)

    def test_샐러리_메뉴_재고_추가(self):
        # given
        menu_lst = list(menu.Menu.objects.all())
        menu_dic = {menu_obj.name: (menu_obj.stock + STOCK_UPDATE_AMOUNT) for menu_obj in menu_lst}
        # when
        tasks.add_menu_stock_to_all()
        # then
        new_menu_lst = list(menu.Menu.objects.all())
        new_menu_dic = {menu_obj.name: menu_obj.stock for menu_obj in new_menu_lst}
        self.assertDictEqual(menu_dic, new_menu_dic)

    def test_샐러리_유저_포인트_추가(self):
        # given
        user_lst = list(User.objects.all())
        user_dic = {user_obj.username: (user_obj.coffee_point + POINT_UPDATE_AMOUNT) for user_obj in user_lst}
        # when
        tasks.add_user_point_to_all()
        # then
        new_user_lst = list(User.objects.all())
        new_user_dic = {user_obj.username: user_obj.coffee_point for user_obj in new_user_lst}
        self.assertDictEqual(user_dic, new_user_dic)
