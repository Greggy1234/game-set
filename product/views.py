from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Category, Tag, Product, Review
from .forms import ReviewForm

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
    reviews = Review.objects.filter(product=product).order_by('-created_on')
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    review_count = reviews.count()
    
    review_form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'review_count': review_count,
        'review_form': review_form
    }
    
    return render(request, 'product/product-detail.html', context)


def add_to_bag(request, sku):
    """
    Add an item to the shopping bag
    """
    
    product = get_object_or_404(Product, sku=sku)
    quantity = 1
    if 'quantity' in request.POST:
        quantity = request.POST['quantity']
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})
    
    if size:
        if sku in list(bag.keys()):
            if size in bag[sku]['product_sizes'].keys():
                bag[sku]['product_sizes'][size] += quantity
                messages.success(request, f'Increased quantity of {product.name} in size {size.upper()} to {bag[sku]["items_by_size"][size]}')
            else:
                bag[sku]['product_sizes'][size] = quantity
                messages.success(request, f'Added {product.name} in size {size.upper()} to your basket')
        else:
            bag[sku] = {'product_sizes': {size: quantity}}
            messages.success(request, f'Added {product.name} in size {size.upper()} to your basket')
    else:
        if sku in list(bag.keys()):
            bag[sku] += quantity
            messages.success(request, f'Increased quantity of {product.name} to {bag[sku]}')
        else:
            bag[sku] = quantity
            messages.success(request, f'Added {product.name} to your basket')
    
    request.session['bag'] = bag
    
    url = request.META.get['HTTP_REFERER']
    
    return redirect(url)