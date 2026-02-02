from rest_framework import routers
from .viewset import OrderViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls
