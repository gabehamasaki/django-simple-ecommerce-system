from rest_framework import viewsets, response, status
from .models import Order
from .serializers import OrderSerializer
from .tasks import create_order

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Dispatch to Celery task for order creation
        customer_id = request.data.get('customer')
        address_id = request.data.get('address')
        items = request.data.get('items', [])

        task = create_order.delay(customer_id, address_id, items)
        return response.Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)
