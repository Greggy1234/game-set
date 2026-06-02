from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import ShopOrderForm, BookingOrderForm
from .models import ShopOrderLineItem, ShopOrder, BookingOrder, BookingOrderLineItem
from product.models import Product
from book.models import Coach, Court
from user_profile.models import Profile
from user_profile.forms import ProfileInfo
from product.contexts import basket_items
from book.contexts import booking_items
from datetime import datetime
from decimal import Decimal
import stripe
import json

# Create your views here.
@require_POST
def cache_shop_checkout_data(request):
    '''
    Collects and add metadata to Stripe for completion of checkout and 
    returns correct response
    '''
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


@require_POST
def cache_book_checkout_data(request):
    '''
    Collects and add metadata to Stripe for completion of checkout and 
    returns correct response
    '''
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bookings': json.dumps(request.session.get('bookings', {})),
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

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                shop_order_form = ShopOrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except Profile.DoesNotExist:
                shop_order_form = ShopOrderForm()
        else:
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
        booking_order_form = BookingOrderForm(form_data)
        if booking_order_form.is_valid():
            booking_order = booking_order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            booking_order.stripe_pid = pid
            booking_order.original_bookings = json.dumps(bookings)
            booking_order.save()
            for court_id, dates in bookings.items():
                try:
                    court = get_object_or_404(Court, id=court_id)
                    for date, times in dates.items():
                        booking_date = date
                        date_as_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
                        for time, info in times.items():
                            booking_time = time
                            time_as_time = datetime.strptime(booking_time, "%H:%M").time()
                            booking_cost = Decimal(info["cost"])
                            coach_id = info["coach"]
                            booking_coach = None
                            if coach_id and coach_id != "None":
                                booking_coach = get_object_or_404(Coach, id=coach_id)
                            if booking_coach:
                                booking_order_line_item = BookingOrderLineItem (
                                    booking=booking_order,
                                    court=court,
                                    coach=booking_coach,
                                    date=date_as_date,
                                    time=time_as_time,
                                    lineitem_total=booking_cost,
                                )
                                booking_order_line_item.save()
                            else:
                                booking_order_line_item = BookingOrderLineItem (
                                    booking=booking_order,
                                    court=court,
                                    date=date_as_date,
                                    time=time_as_time,
                                    lineitem_total=booking_cost,                                
                                )
                                booking_order_line_item.save()
                except Court.DoesNotExist:
                    messages.error(request, (
                        "A court was not found in our database!")
                    )
                    booking_order.delete()
                    return redirect(reverse('view_bookings'))
                
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('booking_checkout_success', args=[booking_order.booking_number]))
        else:
            messages.error(request, 'Something went wrong! Please check your information.')
    
    else:
        bookings = request.session.get('bookings', {})
        if not bookings:
            messages.error(request, "You haven't made any bookings yet!")
            return redirect(reverse("book_overview"))

        current_bookings = booking_items(request)
        grand_total_bookings = current_bookings['total_booking_amount']
        stripe_total = round(grand_total_bookings * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                booking_order_form = BookingOrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except Profile.DoesNotExist:
                booking_order_form = BookingOrderForm()
        else:
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
    """
    Handle successful SHOP hub checkouts
    
    **Context**
    ``shop_order``
        The correct shop order information taken from :model:`checkout.ShopOrder`

    **Template**
        :template:`checkout/shop-checkout-success.html`
    """
    save_info = request.session.get('save_info')
    shop_order = get_object_or_404(ShopOrder, order_number=order_num)
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        shop_order.user_profile = profile
        shop_order.save()

        if save_info:
            profile_data = {
                'default_phone_number': shop_order.phone_number,
                'default_country': shop_order.country,
                'default_postcode': shop_order.postcode,
                'default_town_or_city': shop_order.town_or_city,
                'default_street_address1': shop_order.street_address1,
                'default_street_address2': shop_order.street_address2,
                'default_county': shop_order.county,
            }
            user_profile_form = ProfileInfo(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
    
    
    messages.success(request, f'Success! Your order number is {order_num}. \
        A confirmation email will be sent to {shop_order.email}.')

    if 'basket' in request.session:
        del request.session["basket"]
    
    context = {
        "shop_order": shop_order,
    }
    
    return render(request, "checkout/shop-checkout-success.html", context)


def booking_checkout_success(request, booking_number):
    """
    Handle successful BOOK hub checkouts
    
    **Context**
    ``booking_order``
        The correct booking information taken from :model:`checkout.BookingOrder`

    **Template**
        :template:`checkout/booking-checkout-success.html`
    """
    save_info = request.session.get('save_info')
    booking_order = get_object_or_404(BookingOrder, booking_number=booking_number)
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        booking_order.user_profile = profile
        booking_order.save()

        if save_info:
            profile_data = {
                'default_phone_number': booking_order.phone_number,
                'default_country': booking_order.country,
                'default_postcode': booking_order.postcode,
                'default_town_or_city': booking_order.town_or_city,
                'default_street_address1': booking_order.street_address1,
                'default_street_address2': booking_order.street_address2,
                'default_county': booking_order.county,
            }
            user_profile_form = ProfileInfo(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
    
    
    messages.success(request, f'Success! Your order number is {booking_number}. \
        A confirmation email will be sent to {booking_order.email}.')

    if 'bookings' in request.session:
        del request.session["bookings"]
    
    context = {
        "booking_order": booking_order,
        "save_info": save_info,
    }
    
    return render(request, "checkout/booking-checkout-success.html", context)