from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleList.as_view(), name='news'),
    path("add-comment/<slug:slug>/", views.add_comment, name='add_comment'),
    path("<slug:slug>/", views.article_detail, name='article'),
]