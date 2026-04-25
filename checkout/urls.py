from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path("shop/", views.shop_checkout, name='shop_checkout'),
    path("book/", views.booking_checkout, name='booking_checkout'),
    path("shop/checkout-success/<str:order_num>/", views.shop_checkout_success, name='shop_checkout_success'),
    path("book/checkout-success/<str:booking_num>/", views.booking_checkout_success, name='booking_checkout_success'),
    path("cache-shop-checkout-data/", views.cache_shop_checkout_data, name='cache_shop_checkout_data'),
    path("cache-booking-checkout-data/", views.cache_book_checkout_data, name='cache_book_checkout_data'),
    path("wh/", webhook, name="webhook"),
]