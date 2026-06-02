from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib import messages
from .models import Article, Comment
from .forms import CommentForm

# Create your views here.
class ArticleList(generic.ListView):
    '''
    Returns all published posts in :model:`news.Article`
    and displays them in a page of ten posts.

    **Context**
    ``article``
        All published instances of :model:`news.Article`
    ``paginate_by``
        Number of posts per page

    **Template:**
        :template:`news/news.html`
    '''
    queryset = Article.objects.filter(status=True).order_by('-published_on')
    template_name = "news/news.html"
    context_object_name = "article"
    paginate_by = 10


def article_detail(request, slug):
    '''
    Displays an individual :model:`news.Article`

    **Context**
    ``article``
        The correct instance of :model:`news.Article`
    ``comment``
        All comments from :model:`news.Article` relating to the correct :model:`news.Article`
    ``user_comment``
        The logged in user's comment
    ``comment_count``
        Number of total comments
    ``comment_form``
        An instance of :form:`news.CommentForm`

    **Template:**
        :template:`news/article.html`
    '''
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
    """ 
    Adds a user comments
    
    **Context**
    ``article``
        The correct instance of :model:`news.Article`
    ``comment_form``
        An instance of :form:`news.CommentForm`
    """
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
        else:
            messages.add_message(
                request, messages.ERROR,
                "Something went wrong posting your comment. Please try again!"
            )
    
    return HttpResponseRedirect(reverse('article', args=[slug]))


def edit_comment(request, comment_id):
    """ 
    Edits a user comments
    
    **Context**
    ``article``
        The single correct article instance of :model:`news.Article`
    ``comment_form``
        The single correct form instance of :form:`news.CommentForm`
    ``comment``
        The single correct comment instance of :model:`news.Comment`
    ``article_slug``
        The slug of the article instance
    """
    comment = get_object_or_404(Comment, id=comment_id)
    article = comment.post
    article_slug = article.slug    
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment.author == request.user:
            if comment_form.is_valid:
                comment = comment_form.save(commit=False)
                comment.article = article
                comment.author = request.user
                comment.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    f'Your edits have been saved for your comment on {article.title}'
                )
            else:
                messages.add_message(
                    request, messages.ERROR,
                    "Something went wrong editing your comment. Please try again!"
                ) 
        else:
            messages.add_message(
                request, messages.ERROR,
                "You can only edit your own comment."
            )        
    
    return HttpResponseRedirect(reverse('article', args=[article_slug]))


def delete_comment(request, comment_id):
    """ 
    Deletes a user comments
    
    **Context**
    ``comment``
        The single correct comment instance of :model:`news.Comment`
    ``article_slug``
        The slug of the article instance
    """
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
            "You can only delete your own comment!"
        )
    
    return HttpResponseRedirect(reverse('article', args=[article_slug]))