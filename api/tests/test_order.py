import time
from celery.contrib.testing.worker import start_worker
from django.test import TransactionTestCase

from accounts.models import User, UserType
from api.models import menu, order
from config.celery import app


class OrderTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(app, perform_ping_check=False) # celery 를 따로 실행시킬 필요 없음. db 도 test db 사용.
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)

    def setUp(self) -> None:
        super().setUp()

        # 유저 생성
        self.alice = User.objects.create(username="멤버1", user_type=UserType.MEMBER, coffee_point=10000)
        self.bob = User.objects.create(username="멤버2", user_type=UserType.MEMBER, coffee_point=10000)
        # 메뉴 생성
        self.coffee = menu.Menu.objects.create(name="커피", price=3000, stock=30)
        self.ade = menu.Menu.objects.create(name="에이드", price=4000, stock=30)

    def test_주문_생성하기(self):
        # given
        self.client.force_login(self.alice)
        # when
        res = self.client.post(
            path="/api/order/",
            content_type="application/json",
            data={
                "menu": "커피",
                "count": 1,
            },
        )
        # then
        self.assertEqual(res.status_code, 201)
        time.sleep(1)
        data = res.json()
        order_obj = order.Order.objects.get(id=data['id'])
        self.assertEqual(order_obj.is_done, True)
