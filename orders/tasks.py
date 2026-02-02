import random
from django.utils import timezone
from django.db import transaction
from datetime import datetime, timedelta
from celery import shared_task
from .models import OrderItem, Order
from core.celery import celery

@shared_task(name="orders.tasks.process_payment")
def process_payment(order_id):
    try:
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            if order.payment_status != 'unpaid':
                return f"Order {order_id} payment already processed"

            # Simula o processamento do pagamento
            payment_successful = random.choice([True, False])

            if payment_successful:
                order.payment_status = 'paid'
                order.paid_at = timezone.now()
                order.save()
            else:
                order.payment_status = 'unpaid'
                order.save()
                return f"Payment failed for order {order_id}"

            celery.send_task("inventory.tasks.payment_confirmation_reservation_release", args=[order_id])
            return f"Payment processed successfully for order {order_id}"


    except Exception as e:
        return str(e)


@shared_task(name="orders.tasks.simulate_payment_webhook")
def simulate_payment_webhook():
    # Get all unpaid orders id
    orders = Order.objects.filter(payment_status='unpaid').values_list('id', flat=True)
    random.shuffle(orders) # Shuffle to simulate randomness

    order = random.choice(orders) if orders else None # Pick a random unpaid order
    if order:
        result = celery.send_task("orders.tasks.process_payment", args=[order])

        return f"Payment webhook simulated for order {order}, task id: {result.id}"
    else:
        return "No unpaid orders found to simulate payment webhook"
