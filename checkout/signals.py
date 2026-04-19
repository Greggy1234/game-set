from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ShopOrderLineItem


@receiver(post_save, sender=ShopOrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem change or creation
    """
    instance.order.update_total()


@receiver(post_delete, sender=ShopOrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem deletion
    """
    instance.order.update_total()