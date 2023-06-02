# from django.conf.urls import url
from django.urls import path, include

from . import views

urlpatterns = [
    path('mesin-antrian', views.mesinantrian, name='mesinantrian'),     # ambil antrian
    path('pemanggil-antrian', views.pemanggilantrian, name='pemanggilantrian'),     # Daftar antrian
    path('<int:pk>/hadir', views.HadirAntrianAdmisiView.as_view()),     # pengakuan pengantri hadir
    path('antrian/pemanggil-antrian/claimantrian', views.claimantrian, name='claimantrian'),       #
    path('antrian/pemanggil-antrian/batalkanantrian', views.batalkanantrian, name='batalkanantrian'),       # batalkan antrian
    path('antrian/pilihloket', views.pilihloket, name='pilihloket'),    # claim loket antrian
    path('autowaktusekarang', views.autowaktusekarang, name='autowaktusekarang'),
    path('automengantri', views.automengantri, name='automengantri'),
    path('ambil-nomor-antrian', views.AmbilAntrianView.as_view())
]
