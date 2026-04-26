from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ShopOrderLineItem, BookingOrderLineItem


@receiver(post_save, sender=ShopOrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on SHOP hub lineitem change or creation
    """
    instance.order.update_shop_total()


@receiver(post_delete, sender=ShopOrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on SHOP hub lineitem deletion
    """
    instance.order.update_shop_total()


@receiver(post_save, sender=BookingOrderLineItem)
def update_on_save_bookings(sender, instance, created, **kwargs):
    """
    Update order total on BOOK hub lineitem creation
    """
    instance.booking.update_bookings_total()


@receiver(post_delete, sender=BookingOrderLineItem)
def update_on_delete_bookings(sender, instance, **kwargs):
    """
    Update order total on BOOK hub lineitem deletion
    """
    instance.booking.update_bookings_total()