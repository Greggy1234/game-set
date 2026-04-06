from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField

# Create your models here.
class Article(models.Model):
    """
    Stores a single blog post entry related to  :model:`auth.User`
    """
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from=['title', 'created_on'])
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    article = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    """
    Stores a single comment related to  :model:`auth.User` and
    :model:`blog.Post`
    """
    post = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"