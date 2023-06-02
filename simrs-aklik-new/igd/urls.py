from django.urls import path

from . import views


urlpatterns = [
    path('pendaftaranigd', views.pendaftaranigd),
    path('caridatapasienvianik', views.caridatapasienvianik),
    path('caridatapasienviabpjs', views.caridatapasienviabpjs),
    path('daftarpasienigd', views.daftarpasienigd),
    path('tambahpasienigdbpjs', views.tambahpasienigdbpjs),
]
