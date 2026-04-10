from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Article, Comment
from .forms import CommentForm

# Create your views here.
class ArticleList(generic.ListView):
    queryset = Article.objects.filter(status=True)
    template_name = "news/news.html"
    context_object_name = "article"
    paginate_by = 10


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comment = Comment.objects.all.filter(post=article)
    user_comment = None
    if request.user.is_authenticated:
        user_comment = comment.filter(user=request.user).first()
    comment_count = comment.count()
    
    comment_form = CommentForm()
    
    context = {
        "article": article,
        "comment": comment,
        "user_comment": user_comment,
        "comment_count": comment_count,
        "comment_form": comment_form,
    }
    
    return render(request, 'news/article.html', context)