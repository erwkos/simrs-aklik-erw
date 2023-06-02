from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register('kecamatan', views.KecamatanViewSet)


urlpatterns = [] + router.urls
