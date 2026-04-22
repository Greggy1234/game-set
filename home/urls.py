from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("add-feedback/", views.add_feedback, name='add_feedback'),
]