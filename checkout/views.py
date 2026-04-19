from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import ShopOrderForm

# Create your views here.
def shop_checkout(request):
    basket = request.session.get("basket")
    if not basket:
        messages.error(request, "Your basket is empty at the moment. Select some products first!")
        return redirect(reverse("shop"))

    shop_order_form = ShopOrderForm()
    context = {
        "shop_order_form": shop_order_form,
    }
    
    return render(request, "checkout/shop-checkout.html", context)
