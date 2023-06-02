from django.urls import path


from . import views
from antrian import views as views_antrian


urlpatterns = [
    path('ambil-antrian', views_antrian.mesinantrian),
    path('antrian-admisi', views_antrian.pemanggilantrian),
    path('pendaftaran/rawat-jalan/<int:pk>', views.PendaftarnRawatJalanPasienBaruView.as_view()),
    path('pendaftaran/rawat-jalan/pasien-lama/<int:pk>', views.PendaftarnRawatJalanPasienLamaView.as_view())
]
