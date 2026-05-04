from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import ShopOrder, ShopOrderLineItem, BookingOrder, BookingOrderLineItem
from user_profile.models import Profile
from product.models import Product
from book.models import Coach, Court
import stripe
import time
import json
from datetime import datetime
from decimal import Decimal

import logging
logger = logging.getLogger(__name__)


class StripeWH_Handler:
    """Handle webhooks from Stripe"""

    def __init__(self, request):
        self.request = request
    
    def _send_confirmation_email(self, item, type):
        """Send the user a confirmation email"""
        cust_email = item.email
        if type == "basket":
            subject = render_to_string(
                'checkout/confirmation_emails/shop_confirmation_email_subject.txt',
                {'shop_order': item})
            body = render_to_string(
                'checkout/confirmation_emails/shop_confirmation_email_body.txt',
                {'shop_order': item, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        elif type == "booking":
            subject = render_to_string(
                'checkout/confirmation_emails/book_confirmation_email_subject.txt',
                {'book_order': item})
            body = render_to_string(
                'checkout/confirmation_emails/book_confirmation_email_body.txt',
                {'book_order': item, 'contact_email': settings.DEFAULT_FROM_EMAIL})
                    
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )
        
    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200)
    
    def handle_payment_intent_succeeded(self, event):    
        intent = event.data.object
        logger.error(f"Full metadata: {intent.metadata}")
        pid = intent.id
        logger.error(f"Intent PID: {pid}")
        if intent.metadata.basket:
            basket = intent.metadata.basket
        elif intent.metadata.bookings:
            bookings = intent.metadata.bookings
        save_info = intent.metadata.save_info
        
        charge = stripe.Charge.retrieve(intent.latest_charge)

        billing_details = charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(charge.amount / 100, 2)
        
        for field, value in shipping_details.address.to_dict().items():
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
        
        if intent.metadata.basket:
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
                self._send_confirmation_email(shop_order, "basket")
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                    status=200)
            else:
                shop_order = None
                try:
                    shop_order = ShopOrder.objects.create(
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
                                    product_size=size,
                                )
                                shop_order_lineitem.save()
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
            self._send_confirmation_email(shop_order, "basket")
            return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
        elif intent.metadata.bookings:
            booking_order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    booking_order = BookingOrder.objects.get(
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
                        original_bookings=bookings,
                        stripe_pid=pid,
                    )
                    booking_order_exists = True
                    break
                except BookingOrder.DoesNotExist:
                    attempt += 1
                    time.sleep(1)
            if booking_order_exists:
                self._send_confirmation_email(booking_order, "booking")
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified booking already in database',
                    status=200)
            else:
                booking_order = None
                try:
                    booking_order = BookingOrder.objects.create(
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
                        original_bookings=bookings,
                        stripe_pid=pid,
                    )
                    for court_id, dates in json.loads(bookings).items():
                        court = get_object_or_404(Court, id=court_id)
                        for date, times in dates.items():
                            booking_date = date
                            date_as_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
                            for time_slot, info in times.items():
                                booking_time = time_slot
                                time_as_time = datetime.strptime(booking_time, "%H:%M").time()
                                booking_cost = Decimal(info["cost"])
                                coach_id = info["coach"]
                                booking_coach = None
                                if coach_id:
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
                except Exception as e:
                    if booking_order:
                        booking_order.delete()                
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status=500)        
            self._send_confirmation_email(booking_order, "booking")
            return HttpResponse(
                content=f'Webhook received: {event["type"]}',
                status=200)
    
    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)