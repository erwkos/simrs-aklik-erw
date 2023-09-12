from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views
from . import api_views

router = SimpleRouter(trailing_slash=False)
router.register('api/register-klaim', api_views.RegisterKlaimViewSet, basename='api-register-klaim')
router.register('api/data-klaim', api_views.DataKlaimViewSet, basename='api-data-klaim')
router.register('verifikator', api_views.VerifikatorViewSet, basename='verifikator')

urlpatterns = [
    path('daftar-register', views.daftar_register, name='daftar-register'),
    path('detail-register/<int:pk>', views.detail_register, name='detail-register'),
    path('import-data-klaim', views.import_data_klaim, name='import-data-klaim'),
    path('daftar-data-klaim', views.daftar_data_klaim, name='daftar-data-klaim'),
    path('detail-data-klaim/<int:pk>', views.detail_data_klaim, name='detail-data-klaim'),
    path('finalisasi-data-klaim', views.finalisasi_data_klaim, name='finalisasi-data-klaim'),
    path('update/finalisasi-data-klaim/<int:pk>', views.update_finalisasi_data_klaim,
         name='update-finalisasi-data-klaim'),
    path('update/update-data_klaim-cbg/<int:pk>', views.update_data_klaim_cbg, name='update-data-klaim-cbg'),
    path('download/cbg/', views.download_data_cbg, name='download_data_cbg')
] + router.urls
