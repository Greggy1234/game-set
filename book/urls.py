from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_home, name='book_hub'),
    path("coaches/", views.coach_overview, name='coaches'),
    path("court/<int:pk>/", views.court_detail, name='court_detail'),
]