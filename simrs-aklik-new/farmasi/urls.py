from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register('antrian', views.AntrianFarmasiViewSet, basename='antrian')
router.register('api/master-data/obat', views.ApiMasterDataObatViewSet)

urlpatterns = [
    path('antrian-farmasi', views.AntrianFarmasiView.as_view()),
    path('obat-pasien', views.TambahObatPasienRawatJalanView.as_view()),
    path('obat-pasien/<int:pk>/hapus', views.HapusObatPasienView.as_view()),
    path('siapkan-obat/<int:pk>', views.SiapkanObatPasienView.as_view()),
    path('detail-obat-pasien/<int:pk>', views.DetailObatPasienView.as_view()),
    path('konfirm-obat-diterima/<int:pk>', views.KonfirmObatDiterimaView.as_view()),

    # master data
    path('master-data/daftar-obat', views.MasterDataObatView.as_view()),
    path('master-data/detail-obat/<int:pk>', views.MasterDataDetailObatView.as_view()),
    path('master-data/tambah-obat', views.MasterDataTambahObatView.as_view())
] + router.urls
