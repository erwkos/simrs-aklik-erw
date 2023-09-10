from django.urls import include, path

from . import views

app_name = 'supervisor'

urlpatterns = [
    path('daftar-register/', views.daftar_register_supervisor, name='daftar_register_supervisor'),
    path('detail-register/<int:pk>', views.detail_register_supervisor, name='detail_register_supervisor'),
    # path('pembagian-ulang/', views.pembagian_ulang, name='claim_bagi_ulang'),
    path('daftar/pembagian-ulang-verifikasi-cbg/', views.daftar_pembagian_ulang_verifikasi_cbg,
         name='daftar_pembagian_ulang_verifikasi_cbg'),
    path('pembagian-ulang-verifikasi-cbg/<int:pk>', views.update_pembagian_ulang_verifikasi_cbg,
         name='update_pembagian_ulang_verifikasi_cbg'),
    path('api/json/pembagian/data/klaim/cbg/', views.api_json_pembagian_data_klaim_cbg,
         name='api_json_pembagian_data_klaim_cbg'),

]
