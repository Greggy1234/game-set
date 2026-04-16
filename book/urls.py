from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_overview, name='book_overview'),
    path("coaches/", views.coach_overview, name='coaches'),
    path("court/<slug:slug>/", views.court_detail, name='court_detail'),
]