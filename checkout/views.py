from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import ShopOrderForm
from product.contexts import basket_items
import stripe

# Create your views here.
def shop_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
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
