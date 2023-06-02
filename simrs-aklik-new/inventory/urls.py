from django.urls import path

from . import views

urlpatterns = [
    path('tambah-alkes-pasien', views.TambahLayananMonitoringView.as_view()),
    path('hapus-alkes/pasien/<int:pk>', views.HapusAlatKesehatanPasienView.as_view())
]