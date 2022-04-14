from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename="user")
router.register(r'menu', views.MenuViewSet, basename='menu')
router.register(r'order', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
