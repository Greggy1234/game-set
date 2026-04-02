from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_products, name='shop'),
    path("basket/", views.basket, name='basket'),
    path("add-to-basket/", views.add_to_basket, name='add_to_basket'),
    path("remove-from-basket/<str:sku>/", views.remove_from_basket, name='remove_from_basket'),
    path("<str:sku>/", views.product_detail, name='product_detail'),
]