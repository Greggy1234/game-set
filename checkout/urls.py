from django.urls import path
from . import views

urlpatterns = [
    path("shop/", views.shop_checkout, name='shop_checkout'),
]