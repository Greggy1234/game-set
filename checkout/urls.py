from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path("shop/", views.shop_checkout, name='shop_checkout'),
    path("shop/checkout-success/<str:order_num>/", views.shop_checkout_success, name='shop_checkout_success'),
    path("cache-shop-checkout-data/", views.cache_shop_checkout_data, name='cache_shop_checkout_data'),
    path("wh/", webhook, name="webhook"),
]