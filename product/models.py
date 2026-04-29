from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django_extensions.db.fields import AutoSlugField

# Create your models here.
class Category(models.Model):
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    tag = models.ForeignKey('Tag', null=True, blank=True, on_delete=models.SET_NULL)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    image_name = models.CharField(max_length=254, null=True, blank=True)
    show_on_site = models.BooleanField(default=True)
    
    
    def avg_rating(self):
        """
        Update rating with average of all reviews
        """
        ratings = self.review_product.all()
        non_zero_ratings = []
        for rat in ratings:
            if rat.rating > 0:
                non_zero_ratings.append(rat.rating)
        if non_zero_ratings:
            average = sum(non_zero_ratings)/len(non_zero_ratings)
            average_round = round(average, 2)
            self.rating = average_round
        else:
            self.rating = None
        self.save()


    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Stores a single instance of a review entry,
    related to :model:`product.Product` and :model:`auth.User`
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review_user"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="review_product"
    )
    review = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[
                                     MinValueValidator(0.00),
                                     MaxValueValidator(5.00)
                                 ], blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from=['user__username', 'product__sku', 'id'])
    
    
    def save(self, *args, **kwargs):
        """
        Call the avg_rating method
        """
        super().save(*args, **kwargs)
        self.product.avg_rating()
    
    
    def __str__(self):
        return f'Review of {self.product} by {self.user}'