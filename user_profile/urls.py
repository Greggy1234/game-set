from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/", views.user_profile, name='user_profile'),
    path("<str:username>/update-years/", views.update_years, name='update_years'),
    path("<str:username>/update-surface/", views.update_surface, name='update_surface'),
    path("<str:username>/update-shot/", views.update_shot, name='update_shot'),
]