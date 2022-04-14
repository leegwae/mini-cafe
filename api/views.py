import random
import time

from celery import shared_task
from django.db import transaction, DatabaseError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from .models import menu, order, user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = user.UserSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = menu.Menu.objects.all()
    serializer_class = menu.MenuSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = order.Order.objects.all()
    serializer_class = order.OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                count = int(request.data['count'])
                # 재고 차감
                menu_obj = get_object_or_404(menu.Menu, name=request.data['menu'])
                if count <= menu_obj.stock:
                    menu_obj.stock -= count
                else:
                    raise ValidationError(detail="재고가 부족합니다", code="no_stocks")
                menu_obj.save()
                # 포인트 차감
                user_obj = request.user
                if count * menu_obj.price <= user_obj.coffee_point:
                    user_obj.coffee_point -= (count * menu_obj.price)
                else:
                    raise ValidationError(detail="유저 포인트가 부족합니다", code="no_points")
                user_obj.save()
                # 주문 저장
                self.perform_create(serializer)
            # 태스크 추가 & 주문 상태 업데이트
            order_in_progress.delay(serializer.data)
        except DatabaseError:
            # You may need to manually revert model state when rolling back a transaction.
            return Response({"message": "DB 에러"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # except Exception:
        #     return Response({"message": "예외 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

@shared_task
def order_in_progress(order_dic):
    # 주문 개수만큼 시간 늘어남
    time.sleep(order_dic['count'] * random.randrange(1, 3))
    # 주문 완료 표시
    order_obj = order.Order.objects.get(pk=order_dic['pk'])
    order_obj.is_done = True
    order_obj.save()

