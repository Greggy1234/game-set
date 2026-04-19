from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import ShopOrderForm
import stripe

# Create your views here.
def shop_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    basket = request.session.get("basket")
    if not basket:
        messages.error(request, "Your basket is empty at the moment. Select some products first!")
        return redirect(reverse("shop"))

    stripe.api_key = stripe_secret_key

    shop_order_form = ShopOrderForm()
    context = {
        "shop_order_form": shop_order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": "Test value",
        
    }
    
    return render(request, "checkout/shop-checkout.html", context)
