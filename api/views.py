from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from api.models import menu, order, user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user.UserSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = menu.Menu.objects.all()
    serializer_class = menu.MenuSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = order.Order.objects.all()
    # queryset = order.Order.objects.prefetch_related('user').all()
    serializer_class = order.OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 잔여 포인트 확인
        self.check_point(request.data)
        # 재고 확인
        self.check_stock(request.data)
        # DB 변경
        with transaction.atomic():
            # 포인트 차감
            # 재고 차감
            # 주문 저장
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def check_point(self, data):
        pass

    @transaction.atomic
    def check_stock(self, data):
        print("check_stock", data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
