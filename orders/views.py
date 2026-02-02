from rest_framework import viewsets, status
from rest_framework.response import Response
from core.celery import celery
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        # Salva o pedido no PostgreSQL
        order = serializer.save()

        # Salva o snapshot do endereço
        order.address_snapshot = str(order.address)
        order.save()

        # Dispara o evento para o RabbitMQ
        celery.send_task("inventory.tasks.reserve_stock", args=[str(order.id)])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
