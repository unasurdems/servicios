from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ServicioModelViewSet

api_router = DefaultRouter()

api_router.register(r'servicio', ServicioModelViewSet, base_name='servicio_servicios')

urlpatterns = [
    url(r'^api/', include(api_router.urls)),
]