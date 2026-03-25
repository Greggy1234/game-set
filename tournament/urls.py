from django.urls import path
from . import views

urlpatterns = [
    path("", views.tournament_home, name='match'),
    path("<str:tour>-calendar/", views.calendar, name='tour_calendar'),
    path("<str:tour>-calendar/<slug:slug>/", views.tournament_detail, name='tournament_detail'),
]