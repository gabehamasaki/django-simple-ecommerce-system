from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/', include('orders.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Endpoints da Documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # UI do Swagger:
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # UI do Redoc (alternativa):
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
