from django.urls import path

from . import views


urlpatterns = [
    path('antrian-dokter', views.AntrianDokterRawatJalanView.as_view()),
    path('rawat-jalan/<int:pk>/selesai', views.SelesaiLayananView.as_view())
]