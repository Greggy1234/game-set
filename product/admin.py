from django.contrib import admin
from .models import Category, Tag, Product, Review

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    
    
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'created_on',
    )


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = (
        'category',
        'tag',
        'sku',
    )
    
    list_display = (
        'name',
        'category',
        'tag',
        'sku',
        'price',
    )


admin.site.register(Category, CategoryAdmin),
admin.site.register(Tag, TagAdmin),
admin.site.register(Review, ReviewAdmin),
admin.site.register(Product, ProductAdmin),