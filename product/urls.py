from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_products, name='shop'),
    path("add-to-basket", views.add_to_basket, name='add-to-basket')
    path("<str:sku>/", views.product_detail, name='product_detail'),
]