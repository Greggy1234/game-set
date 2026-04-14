from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleList.as_view(), name='news'),
    path("<slug:slug>/", views.article_detail, name='article'),
]