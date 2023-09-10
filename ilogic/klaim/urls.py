from django.urls import path

from rest_framework.routers import SimpleRouter

from .api_views import (
    MonitoringDataKlaimViewSet
)

router = SimpleRouter(trailing_slash=False)
router.register('api/monitoring/data-klaim', MonitoringDataKlaimViewSet)

urlpatterns = [
] + router.urls
