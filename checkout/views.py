from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import ShopOrderForm, BookingOrderForm
from .models import ShopOrderLineItem, ShopOrder, BookingOrder, BookingOrderLineItem
from product.models import Product
from product.contexts import basket_items
from book.contexts import booking_items
import stripe
import json

# Create your views here.
@require_POST
def cache_shop_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def shop_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    if request.method == "POST":
        basket = request.session.get("basket")
        
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        shop_order_form = ShopOrderForm(form_data)
        if shop_order_form.is_valid():
            shop_order = shop_order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            shop_order.stripe_pid = pid
            shop_order.original_basket = json.dumps(basket)
            shop_order.save()
            for sku, info in basket.items():
                try:
                    if not isinstance(info, int):
                        product = get_object_or_404(Product, sku=sku)
                        for size, quan in info['product_sizes'].items():
                            shop_order_line_item = ShopOrderLineItem(
                                order=shop_order,
                                product=product,
                                quantity=quan,
                                product_size=size,
                            )
                            shop_order_line_item.save()
                    else:
                        product = get_object_or_404(Product, sku=sku)
                        shop_order_line_item = ShopOrderLineItem(
                            order=shop_order,
                            product=product,
                            quantity=info,
                        )
                        shop_order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "A product was not found in our database!")
                    )
                    shop_order.delete()
                    return redirect(reverse('basket'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('shop_checkout_success', args=[shop_order.order_number]))
        else:
            messages.error(request, 'Something went wrong! Please check your information.')
        
    else:
        basket = request.session.get("basket")
        if not basket:
            messages.error(request, "Your basket is empty at the moment. Select some products first!")
            return redirect(reverse("shop"))

        current_basket = basket_items(request)
        grand_total = current_basket['grand_total']
        stripe_total = round(grand_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        shop_order_form = ShopOrderForm()

        if not stripe_public_key:
            messages.warning(request, 'No public key was set for Stripe. Please set this first!')    

        context = {
            "shop_order_form": shop_order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
            
        }

        return render(request, "checkout/shop-checkout.html", context)


def booking_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    if request.method == "POST":
        bookings = request.session.get('bookings', {})
        
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': "GB",
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        } 
    
    else:
        bookings = request.session.get('bookings', {})
        if not bookings:
            messages.error(request, "You haven't made any bookings yet!")
            return redirect(reverse("book_overview"))

        current_bookings = booking_items(request)
        grand_total_bookings = current_bookings['total_booking_amount']
        print(grand_total_bookings)
        stripe_total = round(grand_total_bookings * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        booking_order_form = BookingOrderForm()

        if not stripe_public_key:
            messages.warning(request, 'No public key was set for Stripe. Please set this first!')    

        context = {
            "booking_order_form": booking_order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,            
        }

        return render(request, "checkout/booking-checkout.html", context)


def shop_checkout_success(request, order_num):
    save_info = request.session.get('save_info')
    shop_order = get_object_or_404(ShopOrder, order_number=order_num)
    messages.success(request, f'Success! Your order number is {order_num}. \
        A confirmation email will be sent to {shop_order.email}.')

    if 'basket' in request.session:
        del request.session["basket"]
    
    context = {
        "shop_order": shop_order,
        "save_info": save_info,
    }
    
    return render(request, "checkout/shop-checkout-success.html", context)