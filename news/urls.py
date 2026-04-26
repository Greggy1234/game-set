from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleList.as_view(), name='news'),
    path("add-comment/<slug:slug>/", views.add_comment, name='add_comment'),
    path("edit-comment/<int:comment_id>/", views.edit_comment, name='edit_comment'),
    path("delete-comment/<int:comment_id>/", views.delete_comment, name='delete_comment'),
    path("<slug:slug>/", views.article_detail, name='article'),
]