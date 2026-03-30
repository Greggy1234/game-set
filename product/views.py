from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Category, Tag, Product

# Create your views here.
def all_products(request):
    """
    Brings all the products into a single page. Allows for sorting, refining and searching
    
    **Template**
        :template:`product/shop.html`
    """
    
    products = Product.objects.all()
    query = None
    tag = None
    sort = None
    direction = None
    current_category = None
    
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'No search criteria entered!')
                return redirect(reverse('shop'))
        
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        
        if 'category' in request.GET:
            cat = request.GET['category']
            products = products.filter(category__name=cat)
            current_category = cat
            
        if 'tag' in request.GET:
            tag= request.GET['tag'].split(",")
            products = products.filter(tag__name__in=tag)
        
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'products': products,
        'user_query': query,
        'tags': tags,
        'current_sorting': current_sorting,
        'categories': categories,
        'current_category': current_category,
    }
    
    return render(request, 'product/shop.html', context)

def product_detail(request, sku):
    """
    Shows the product selected by the user
    """
    
    product = get_object_or_404(Product, sku=sku)
    
    context = {
        'product': product,
    }
    
    return render(request, 'product/product_detail.html', context)