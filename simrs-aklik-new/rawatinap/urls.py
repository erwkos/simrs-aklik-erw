from django.urls import path

from . import views


urlpatterns = [
    path('mutasirawatinap', views.mutasirawatinap),
    path('caridatapasienvianik', views.caridatapasienvianik),
    path('caridatapasienviabpjs', views.caridatapasienviabpjs),
    path('daftarpasienrawatinap', views.daftarpasienrawatinap),
    path('postmutasirawatinap', views.postmutasirawatinap),
]
