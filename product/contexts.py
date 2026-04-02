from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from product.models import Product


def basket_items(request):
    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})
    
    for sku, info in basket.items():
        if 'product_sizes' in info:
            product = get_object_or_404(Product, sku=sku)
            for size, quan in info['product_sizes']:
                total += quan * product.price
                product_count += quan
                basket_items.append({
                    'sku': sku,
                    'quantity': quan,
                    'product': product,
                    'size': size,
                })
        else:
            product = get_object_or_404(Product, sku=sku)
            total += info * product.price
            product_count += info
            basket_items.append({
                'sku': sku,
                'quantity': info,
                'product': product,
            })
            
            
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery = 0
    
    grand_total = delivery + total
    
    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery': free_delivery,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    
    return context