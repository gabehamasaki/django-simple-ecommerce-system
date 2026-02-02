from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from core.celery import celery

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        # Dispara a tarefa de reserva de estoque
        celery.send_task('inventory.tasks.reserve_stock', args=[str(instance.id)])
        celery.send_task('orders.tasks.update_total_amount', args=[str(instance.id)])
