from django.contrib import admin
from .models import ShopOrder, ShopOrderLineItem

# Register your models here.
class ShopLineItemsInline(admin.TabularInline):
    model = ShopOrderLineItem
    readonly_fields = ("lineitem_total",)


class OrderAdmin(admin.ModelAdmin):
    inlines = (ShopLineItemsInline,)
    
    readonly_fields = ("order_number", "date", "delivery_cost", "order_total", "grand_total",)
    
    list_display = ("order_number", "date", "full_name", "order_total", "delivery_cost", "grand_total",)
    
    orderin = ("-date")
    
admin.site.register(ShopOrder, OrderAdmin)