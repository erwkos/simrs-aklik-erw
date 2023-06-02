from django.urls import path

from . import views

urlpatterns = [
    path('request/layanan-radiologi/rawat-jalan', views.RequestLayananRadiologiPasienRawatJalan.as_view()),
    path('antrian-radiologi', views.AntrianLayananRadiologiView.as_view()),
    path('layanan-radiologi-batalkan/<int:pk>', views.BatalkanLayananRadiologiPasienView.as_view()),
    path('layanan-radiologi-hadir/<int:pk>', views.HadirLayananRadiologiView.as_view()),
    path('layanan-radiologi-laporan/<int:pk>', views.LaporanLayananRadiologiView.as_view()),
    path('layanan-radiologi/<int:pk>/selesai', views.SelesaiLaporanLayananRadiologi.as_view()),
    path('rawat-jalan/hasil/<int:pk>', views.HasilLaporanRadiologiPasienView.as_view())
]