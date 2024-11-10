from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views
from . import api_views
from .views import RumahSakitAutocomplete

router = SimpleRouter(trailing_slash=False)
router.register('api/register-klaim', api_views.RegisterKlaimViewSet, basename='api-register-klaim')
router.register('api/register-klaim-obat', api_views.RegisterKlaimObatViewSet, basename='api-register-klaim-obat')

router.register('api/data-klaim', api_views.DataKlaimViewSet, basename='api-data-klaim')
router.register('verifikator', api_views.VerifikatorViewSet, basename='verifikator')

urlpatterns = [
      path('daftar-register', views.daftar_register, name='daftar-register'),
      path('detail-register/<int:pk>', views.detail_register, name='detail-register'),
      path('import-data-klaim', views.import_data_klaim, name='import-data-klaim'),
      path('daftar-data-klaim', views.daftar_data_klaim, name='daftar-data-klaim'),

      path('cek-aksi-vibi-vidi', views.cek_aksi_vibi_vidi, name='cek-aksi-vibi-vidi'),
      path('sinkronisasi-aksi-vibi-vidi', views.sinkronisasi_aksi_vibi_vidi,
           name='sinkronisasi-aksi-vibi-vidi'),
      path('sinkronisasi-vibi-vidi/download', views.sinkronisasi_vibi_vidi_download,
           name='sinkronisasi-vibi-vidi-download'),

      path('detail-data-klaim/<int:pk>', views.detail_data_klaim, name='detail-data-klaim'),
      path('finalisasi-data-klaim', views.finalisasi_data_klaim, name='finalisasi-data-klaim'),
      path('update/finalisasi-data-klaim/<int:pk>', views.update_finalisasi_data_klaim,
           name='update-finalisasi-data-klaim'),
      path('update/update-data_klaim-cbg/<int:pk>', views.update_data_klaim_cbg,
           name='update-data-klaim-cbg'),
      path('download/cbg/', views.download_data_cbg, name='download_data_cbg'),

      # autocomplete
      path('api/rumahsakit-autocomplete/', RumahSakitAutocomplete.as_view(),
           name='rumahsakit-autocomplete'),

      # obat
      path('import-data-klaim-obat', views.import_data_klaim_obat, name='import-data-klaim-obat'),
      path('daftar-data-klaim-obat', views.daftar_data_klaim_obat, name='daftar-data-klaim-obat'),
      path('detail-data-klaim-obat/<int:pk>', views.detail_data_klaim_obat, name='detail-data-klaim-obat'),
      path('download/obat/', views.download_data_obat, name='download_data_obat'),

      # fitur fragmentasi, readmisi, dan rehabilitasi
      path('fragmentasi', views.fragmentasi, name='fragmentasi'),
      path('simpan-status-fragmentasi/', views.simpan_status_fragmentasi, name='simpan_status_fragmentasi'),
      path('detail-data-klaim-verifkhusus/<str:no_sep>/', views.detail_data_klaim_verifkhusus,
           name='detail_data_klaim_verifkhusus'),
      path('readmisi', views.readmisi, name='readmisi'),
      path('simpan-status-readmisi/', views.simpan_status_readmisi, name='simpan_status_readmisi'),
      path('rehabilitasi', views.rehabilitasi, name='rehabilitasi'),
      path('simpan-status-rehabilitasi/', views.simpan_status_rehabilitasi,
           name='simpan_status_rehabilitasi'),
      path('fragmentasi/detail/', views.get_fragmentasi_detail, name='get_fragmentasi_detail'),
      path('readmisi/detail/', views.get_readmisi_detail, name='get_readmisi_detail'),
      path('rehabilitasi/detail/', views.get_rehabilitasi_detail, name='get_rehabilitasi_detail'),

              ] + router.urls
