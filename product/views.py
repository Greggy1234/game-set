from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Category, Tag, Product, Review
from .forms import ReviewForm, ProductFormEdit, ProductFormAdd

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
    if not product.show_on_site:
        messages.error(request, 'That product is currently unavailable.')
        return redirect(reverse('shop'))
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


def basket(request):
    """
    Renders the current session basket
    """
    quantity_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    context = {
        'quantity_values': quantity_values
    }
    return render(request, 'product/basket.html', context)


def add_to_basket(request):
    """
    Add a product to the shopping basket
    """
    sku = request.POST.get("sku")
    product = get_object_or_404(Product, sku=sku)
    quantity = 1
    if 'quantity' in request.POST:
        quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_sizes' in request.POST:
        size = request.POST.get('product_sizes')
    basket = request.session.get('basket', {})
    
    if size:
        if sku in list(basket.keys()):
            if size in basket[sku]['product_sizes'].keys():
                basket[sku]['product_sizes'][size] += quantity
                messages.success(request, f'Increased quantity of {product.name} in size {size.upper()} to {basket[sku]["product_sizes"][size]}')
            else:
                basket[sku]['product_sizes'][size] = quantity
                messages.success(request, f'Added {product.name} in size {size.upper()} to your basket')
        else:
            basket[sku] = {'product_sizes': {size: quantity}}
            messages.success(request, f'Added {product.name} in size {size.upper()} to your basket')
    else:
        if sku in list(basket.keys()):
            basket[sku] += quantity
            messages.success(request, f'Increased quantity of {product.name} to {basket[sku]}')
        else:
            basket[sku] = quantity
            messages.success(request, f'Added {product.name} to your basket')
    
    request.session['basket'] = basket
    
    url = request.META.get('HTTP_REFERER')
    
    return redirect(url)


def update_quantity(request, sku):
    """
    Add a product to the shopping basket
    """
    product = get_object_or_404(Product, sku=sku)
    quantity = int(request.POST.get('quantity_selection'))
    size = None
    if 'size' in request.POST:
        size = request.POST.get('size')
    basket = request.session.get('basket', {})
    
    if size:
        basket[sku]['product_sizes'][size] = quantity
        messages.success(request, f'Changed the quantity of {product.name} in size {size.upper()} to {quantity}')
    else:
        basket[sku] = quantity
        messages.success(request, f'Changed the quantity of {product.name} to {quantity}')

    request.session['basket'] = basket
    
    return HttpResponseRedirect(reverse('basket'))

def remove_from_basket(request, sku):
    """
    Remove a product from the shopping basket
    """
    product = get_object_or_404(Product, sku=sku)
    size = None
    if 'size' in request.POST:
        size = request.POST.get('size')
    basket = request.session.get('basket', {})
    
    if size:
        del basket[sku]['product_sizes'][size]
        if basket[sku]['product_sizes']:
            messages.success(request, f'Removed {product.name} in size {size.upper()} from your basket')
        else:
            basket.pop(sku)
            messages.success(request, f'Removed {product.name} in size {size.upper()} from your basket')
    else:
        basket.pop(sku)
        messages.success(request, f'Removed {product.name} from your basket')
    
    request.session['basket'] = basket
    
    return HttpResponseRedirect(reverse('basket'))


def add_review(request, sku):
    product = get_object_or_404(Product, sku=sku)
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review_form = review_form.save(commit=False)
            review_form.user = request.user
            review_form.product = product
            review_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'Thank you for reviewing {product.name}'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                "Something went wrong posting your review. Please try again!"
            )
    
    return HttpResponseRedirect(reverse('product_detail', args=[sku])) 


def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    product = review.product
    product_sku = product.sku
    
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST, instance=review)
        if review.user == request.user:
            if review_form.is_valid():
                review_form.save(commit=False)
                review_form.user = request.user
                review_form.product = product                    
                review_form.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    f'Your edits have been saved for your review on {product.name}'
                )
            else:
                messages.add_message(
                    request, messages.ERROR,
                    "Something went wrong editing your review. Please try again!"
                )
        else:
            messages.add_message(
                request, messages.ERROR,
                "You can only edit your own review."
            )    
    
    return HttpResponseRedirect(reverse('product_detail', args=[product_sku])) 


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    product_sku = review.product.sku
    
    if review.author == request.user:
        review.delete()
        messages.add_message(
            request, messages.SUCCESS,
            "Your review has now been deleted"
        )
    else:
        messages.add_message(
            request, messages.ERROR,
            "You can only delete your own review!"
        )
    
    return HttpResponseRedirect(reverse('product_detail', args=[product_sku]))

@login_required
def add_product(request, sku):
    """
    Add a product to the SHOP hub
    """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to that page.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, sku=sku)
    if request.method == 'POST':
        form = ProductFormAdd(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product has been added to store!')
            return redirect(reverse('product_detail', args=[product.sku]))
        else:
            messages.error(request, 'Product has not been added to store! Please ensure the form is valid.')
    else:
        form = ProductFormAdd()
    context = {
        'form': form,
    }

    return render(request, 'product/add-product.html', context)


@login_required
def edit_product(request, sku):
    """
    Edit a product currently displayed in the SHOP hub
    """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to that page.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, sku=sku)
    if request.method == 'POST':
        form = ProductFormEdit(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated {product.name}!')
            return redirect(reverse('product_detail', args=[product.sku]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductFormEdit(instance=product)
        messages.info(request, f'You are editing {product.name}')

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'product/edit-product.html', context)


@login_required
def remove_product_from_site(request, sku):
    """
    Remove a product from showing ont he SHOP hub.
    This does not remove the product from the database, only the template.
    """
    if not request.user.is_superuser:
        messages.error(request, 'You do not have access to that page.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, sku=sku)
    try:
        product.show_on_site = False
        messages.success(
            request, 
            f'Successfully removed {product.name} from the site!'
            )
    except Exception as e:
        messages.error(
            request, 
            f'ERROR: {e}. Try again!'
            )
    
    return redirect(reverse('shop'))

@login_required
def show_removed_products(request):
    products = Product.objects.filter(show_on_site=False)
    
    context = {
        "products": products,
    }
    
    return render(request, 'product/hidden-product.html', context)
