from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views
#
#
# router = SimpleRouter(trailing_slash=False)
# router.register('rawat-jalan', views.InvoiceRawatJalanViewSet, basename='invoice-rawat-jalan')
#
urlpatterns = [
    path('antrian-kasir', views.AntrianKasirView.as_view()),
    path('detail-invoice/<int:pk>', views.SumarryInvoiceView.as_view()),
    path('konfirmasi/invoice/<int:pk>/selesai', views.KonfirmasiPembayaranRawatJalan.as_view())
]
