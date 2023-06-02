from django.urls import path

from . import views


urlpatterns = [
    path('layanan-tindakan', views.TambahLayananTindakanView.as_view()),
    path('layanan-edukasi', views.TambahLayananEdukasiView.as_view()),
    path('layanan-monitoring', views.TambahLayananMonitoringView.as_view()),
    path('layanan-konsultasi', views.TambahLayananKonsultasiView.as_view()),

    path('layanan-konsultasi/<int:pk>/hapus', views.HapusLayananKonsultasiView.as_view()),
    path('layanan-monitoring/<int:pk>/hapus', views.HapusLayananMonitoringView.as_view()),
    path('layanan-edukasi/<int:pk>/hapus', views.HapusLayananEdukasiView.as_view()),
    path('layanan-tindakan/<int:pk>/hapus', views.HapusLayananTindakanView.as_view())
]
