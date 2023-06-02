from django.urls import path


from rest_framework.routers import SimpleRouter

from . import views
#
# router = SimpleRouter(trailing_slash=False)
# router.register('assessment/insert', views.PoliViewSet, basename='poli-assessment')
# router.register('antrian', views.AntrianPoliViewSet, basename='antrian')
#
urlpatterns = [
    path('antrian-poli/', views.AntrianPoliView.as_view()),
    # path('soap/<int:antrian>', views.SOAPPoliView.as_view()),
    # path('soap/<int:pk>/kondisi-pasien', views.KondisiPasienView.as_view()),

    # path('antrian-poli-batalkan/<int:antrian>', views.BatalkanAntrianPoliView.as_view()),
    path('antrian-poli-hadir/<int:antrian>', views.HadirAntrianPoliView.as_view())

]
