from django.contrib import admin
from .models import ShopOrder, ShopOrderLineItem, BookingOrder, BookingOrderLineItem

# Register your models here.
class ShopLineItemsInline(admin.TabularInline):
    model = ShopOrderLineItem
    readonly_fields = ("lineitem_total",)


class OrderAdmin(admin.ModelAdmin):
    inlines = (ShopLineItemsInline,)
    
    readonly_fields = ("order_number", "date", "delivery_cost", "order_total", "grand_total", "original_basket", "stripe_pid",)
    
    list_display = ("order_number", "date", "full_name", "order_total", "delivery_cost", "grand_total", )
    
    ordering = ("-date",)


class BookLineItemsInline(admin.TabularInline):
    model = BookingOrderLineItem
    readonly_fields = ("lineitem_total",)


class BookingOrderAdmin(admin.ModelAdmin):
    inlines = (BookLineItemsInline,)
    
    readonly_fields = ("booking_number", "date", "grand_total", "original_bookings", "stripe_pid",)
    
    list_display = ("booking_number", "date", "full_name", "grand_total", )
    
    ordering = ("-date",)
    
admin.site.register(ShopOrder, OrderAdmin)
admin.site.register(BookingOrder, BookingOrderAdmin)