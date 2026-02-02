from datetime import datetime, timedelta, timezone
from django.db import transaction
from celery import shared_task
from .models import Product, ReservedProduct
from orders.models import Order

@shared_task(name="inventory.tasks.reserve_stock")
def reserve_stock(order_id):
    try:
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            items = order.orders_items.all().select_related('product')

            for item in items:
                product = item.product
                if product.stock_quantity >= item.quantity:
                    product.stock_quantity -= item.quantity
                    product.save()
                    ReservedProduct.objects.create(
                        product=product,
                        order=order,
                        reserved_quantity=item.quantity,
                        expires_at=timezone.now() + timedelta(hours=2)
                    )
                else:
                    raise Exception(f"Estoque insuficiente para {product.name}")
        return f"Reserva concluída para pedido {order_id}"
    except Exception as e:
        return str(e)

@shared_task(name="inventory.tasks.release_expired_reservations")
def release_expired_reservations():
    now = timezone.now()
    expired_reservations = ReservedProduct.objects.filter(expires_at__lt=now)
    count = 0

    with transaction.atomic():
        for reservation in expired_reservations:
            product = reservation.product
            product.stock_quantity += reservation.reserved_quantity
            product.save()
            reservation.delete()
            count += 1

    return f"Liberadas {count} reservas expiradas"

@shared_task(name="inventory.tasks.payment_confirmation_reservation_release")
def payment_confirmation_reservation_release(order_id):
    try:
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            items = order.orders_items.all().select_related('product')
            if order.payment_status == 'paid':
                for item in items:
                    reservation = ReservedProduct.objects.filter(
                        product=item.product,
                        reserved_quantity=item.quantity,
                        expires_at__gt=timezone.now()
                    ).first()
                    if reservation:
                        reservation.delete()
                return f"Released reservations for paid order {order_id}"
            elif order.payment_status in ['unpaid', 'refunded']:
                for item in items:
                    product = item.product
                    product.stock_quantity += item.quantity
                    product.save()
                return f"Estoque devolvido para pedido {order.payment_status}: {order_id}"
            return f"Nenhuma ação necessária para o status: {order.payment_status}"
    except Exception as e:
        return str(e)
