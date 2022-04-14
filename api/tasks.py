import random
import time

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction

from accounts.models import User
from config.params import *
from .models import order, menu

logger = get_task_logger(__name__)


@shared_task
def order_in_progress(order_dic):
    logger.info("{0}번 주문 진행중...".format(order_dic['pk']))
    # 주문 개수만큼 시간 늘어남
    time.sleep(order_dic['count'] * random.randrange(MIN_SEC_TIME_PER_ORDER, MAX_SEC_TIME_PER_ORDER))
    # 주문 완료 표시
    order_obj = order.Order.objects.get(pk=order_dic['pk'])
    order_obj.is_done = True
    order_obj.save()
    logger.info("{0}번 주문 완료!".format(order_dic['pk']))


@shared_task
def add_menu_stock_to_all():
    logger.info("메뉴 재고 추가중...")
    menu_lst = menu.Menu.objects.select_for_update(of=('self')).all()
    with transaction.atomic():
        for menu_obj in menu_lst:
            menu_obj.stock += STOCK_UPDATE_AMOUNT
        menu.Menu.objects.bulk_update(menu_lst, ['stock'])
    logger.info("메뉴 재고 추가 완료!")


@shared_task
def add_user_point_to_all():
    logger.info("유저 포인트 추가중...")
    user_lst = User.objects.select_for_update(of=('self')).all()
    with transaction.atomic():
        for user_obj in user_lst:
            user_obj.coffee_point += POINT_UPDATE_AMOUNT
        User.objects.bulk_update(user_lst, ['coffee_point'])
    logger.info("유저 포인트 추가 완료!")
