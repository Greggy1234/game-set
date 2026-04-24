from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_products, name='shop'),
    path("basket/", views.basket, name='basket'),
    path("add-product/", views.add_product, name='add_product'),
    path("add-review/<str:sku>/", views.add_review, name='add_review'),
    path("add-to-basket/", views.add_to_basket, name='add_to_basket'),
    path("delete-review/<int:review_id>/", views.delete_review, name='delete_review'),
    path("edit-review/<int:review_id>/", views.edit_review, name='edit_review'),
    path("remove-from-basket/<str:sku>/", views.remove_from_basket, name='remove_from_basket'),
    path("remove-product-from-site/<str:sku>/", 
         views.remove_product_from_site, name='remove_product_from_site'),
    path("update-quantity/<str:sku>/", views.update_quantity, name='update_quantity'),
    path("<str:sku>/", views.product_detail, name='product_detail'),
    path("<str:sku>/edit/", views.edit_product, name='edit_product'),
]