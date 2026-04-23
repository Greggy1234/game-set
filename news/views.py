from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib import messages
from .models import Article, Comment
from .forms import CommentForm

# Create your views here.
class ArticleList(generic.ListView):
    queryset = Article.objects.filter(status=True).order_by('-published_on')
    template_name = "news/news.html"
    context_object_name = "article"
    paginate_by = 10


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comment = Comment.objects.filter(post=article)
    user_comment = None
    if request.user.is_authenticated:
        user_comment = comment.filter(author=request.user).first()
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


def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = article
            new_comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'Thank you for your comment on {article.title}'
            )
    
    return HttpResponseRedirect(reverse('article', args=[slug]))


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    article_slug = comment.post.slug
    
    if comment.author == request.user:
        comment.delete()
        messages.add_message(
            request, messages.SUCCESS,
            "Your comment has now been deleted"
        )
    else:
        messages.add_message(
            request, messages.ERROR,
            "You can only delete your own review!"
        )
    
    return HttpResponseRedirect(reverse('article', args=[article_slug]))