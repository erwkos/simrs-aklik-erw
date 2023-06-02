from django.urls import path

from . import views


urlpatterns = [
    path('request/layanan-lab/rawat-jalan', views.RequestLayananLabPasienRawatJalan.as_view()),
    path('antrian-lab', views.AntrianLabView.as_view()),
    path('layanan-lab-batalkan/<int:pk>', views.BatalkanLayananLabPasienView.as_view()),
    path('layanan-lab-hadir/<int:pk>', views.HadirLayananLabView.as_view()),
    path('layanan-lab-laporan/<int:pk>', views.LaporanLayananLabView.as_view()),
    path('layanan-lab/<int:pk>/selesai', views.SelesaiLaporanLayananLabView.as_view()),
    path('rawat-jalan/hasil/<int:pk>', views.HasilLaporanLayananLabPasien.as_view())
]