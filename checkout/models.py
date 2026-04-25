import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from product.models import Product
from book.models import Court, Coach
from user_profile.models import Profile


class ShopOrder(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="shop_orders")
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)    
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    
    def _generate_shop_order_number(self):
        """
        Generate a random, unique order number
        """
        return uuid.uuid4().hex.upper()
    
    def update_shop_total(self):
        """
        Update grand total each time a line item is added including delivery
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()
        
    def numb_of_items(self):
        numb_of_items = self.lineitems.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return numb_of_items
    
    def save(self, *args, **kwargs):
        """
        Set order number if it hasn't been set yet
        """
        if not self.order_number:
            self.order_number = self._generate_shop_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_number}: {self.grand_total}'


class ShopOrderLineItem(models.Model):
    order = models.ForeignKey(ShopOrder, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    
    def save(self, *args, **kwargs):
        """
        Set lineitem total
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name}: {self.product.sku} on order {self.order.order_number}'


class BookingOrder(models.Model):
    booking_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="booking_orders")
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='GB', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)    
    original_bookings = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    
    def _generate_booking_order_number(self):
        """
        Generate a random, unique order number
        """
        return uuid.uuid4().hex.upper()
    
    def update_bookings_total(self):
        """
        Update grand total each time a line item is added
        """
        self.grand_total = self.booking_lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.save()

    def numb_of_bookings(self):
        numb_of_bookings = self.booking_lineitems.objects.count()
        return numb_of_bookings
    
    def save(self, *args, **kwargs):
        """
        Set order number if it hasn't been set yet
        """
        if not self.order_number:
            self.order_number = self._generate_booking_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order_number}: {self.grand_total}'


class BookingOrderLineItem(models.Model):
    booking = models.ForeignKey(BookingOrder, null=False, blank=False, on_delete=models.CASCADE, 
                              related_name='booking_lineitems')
    court = models.ForeignKey(Court, null=False, blank=False, on_delete=models.CASCADE, 
                              related_name="court_lineitems")
    coach = models.ForeignKey(Coach, null=True, blank=True, on_delete=models.CASCADE, 
                              related_name="coach_lineitems")
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    lineitem_total = models.IntegerField(null=False, blank=False, editable=False)
    
    def __str__(self):
        coach_booked = "No coach booked"
        if self.coach:
            coach_booked = self.coach.name        
        
        return f'Booking for {self.court.name} on {self.date} at \
            {self.time} with {coach_booked}. Order number: {self.booking.booking_number}'