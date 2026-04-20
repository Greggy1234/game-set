from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import ShopOrder, ShopOrderLineItem
from user_profile.models import Profile
from product.models import Product
import stripe
import time
import json


class StripeWH_Handler:
    """Handle webhooks from Stripe"""

    def __init__(self, request):
        self.request = request
        
    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200)
    
    def handle_payment_intent_succeeded(self, event):
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info
        
        charge = stripe.Charge.retrieve(intent.latest_charge)

        billing_details = charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(charge.amount / 100, 2)
        
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = Profile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()
        
        shop_order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                shop_order = ShopOrder.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                shop_order_exists = True
                break
            except ShopOrder.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if shop_order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            shop_order = None
            try:
                shop_order = ShopOrder.objects.get(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                for sku, info in json.loads(basket).items():
                    if not isinstance(info, int):
                        product = get_object_or_404(Product, sku=sku)
                        for size, quan in info['product_sizes'].items():
                            shop_order_lineitem = ShopOrderLineItem(
                                order=shop_order,
                                quantity=quan,
                                product=product,
                                product_size=size
                            )
                    else:
                        product = get_object_or_404(Product, sku=sku)
                        shop_order_lineitem = ShopOrderLineItem(
                            order=shop_order,
                            quantity=info,
                            product=product,
                        )
                        shop_order_lineitem.save()
            except Exception as e:
                if shop_order:
                    shop_order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
    
    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)