import random
import sys
import time

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction

from accounts.models import User
from config.params import *
from .models import order, menu

logger = get_task_logger(__name__)
TEST = 'test' in sys.argv


@shared_task
def order_in_progress(order_dic):
    logger.info("{0}번 주문 진행중...".format(order_dic['id']))
    # 주문 개수만큼 시간 늘어남
    if not TEST:
        time.sleep(order_dic['count'] * random.randrange(MIN_SEC_TIME_PER_ORDER, MAX_SEC_TIME_PER_ORDER))
    # 주문 완료 표시
    order_obj = order.Order.objects.get(id=order_dic['id'])
    order_obj.is_done = True
    order_obj.save()
    logger.info("{0}번 주문 완료!".format(order_dic['id']))


@shared_task
def add_menu_stock_to_all():
    logger.info("메뉴 재고 추가중...")
    with transaction.atomic():
        menu_lst = list(menu.Menu.objects.select_for_update().all())
        for menu_obj in menu_lst:
            menu_obj.stock += STOCK_UPDATE_AMOUNT
        menu.Menu.objects.bulk_update(menu_lst, ['stock'])
    logger.info("메뉴 재고 추가 완료!")


@shared_task
def add_user_point_to_all():
    logger.info("유저 포인트 추가중...")
    with transaction.atomic():
        user_lst = list(User.objects.select_for_update().all())
        for user_obj in user_lst:
            user_obj.coffee_point += POINT_UPDATE_AMOUNT
        User.objects.bulk_update(user_lst, ['coffee_point'])
        time.sleep(60)
    logger.info("유저 포인트 추가 완료!")
