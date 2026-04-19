from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_overview, name='book_overview'),
    path("coaches/", views.coach_overview, name='coaches'),
    path("add-booking/", views.add_booking, name='add_booking'),
    path("<slug:slug>/", views.court_book, name='court_book'),
]