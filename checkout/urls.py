from django.urls import path
from . import views

urlpatterns = [
    path("shop/", views.shop_checkout, name='shop_checkout'),
    path("shop/checkout-success/<str:order_num>/", views.shop_checkout_success, name='shop_checkout_success'),
]