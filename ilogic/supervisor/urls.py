from django.urls import include, path

from . import views

app_name = 'supervisor'

urlpatterns = [
    path('daftar-register/', views.daftar_register_supervisor, name='daftar_register_supervisor'),
    path('detail-register/<int:pk>', views.detail_register_supervisor, name='detail_register_supervisor'),
    path('daftar/pembagian-ulang-verifikasi-cbg/', views.daftar_pembagian_ulang_verifikasi_cbg,
         name='daftar_pembagian_ulang_verifikasi_cbg'),
    path('daftar/pembagian-ulang-verifikasi-obat/', views.daftar_pembagian_ulang_verifikasi_obat,
         name='daftar_pembagian_ulang_verifikasi_obat'),
    path('pembagian-ulang-verifikasi-cbg/<int:pk>', views.update_pembagian_ulang_verifikasi_cbg,
         name='update_pembagian_ulang_verifikasi_cbg'),
    path('api/json/pembagian/data/klaim/cbg/', views.api_json_pembagian_data_klaim_cbg,
         name='api_json_pembagian_data_klaim_cbg'),
    path('list/user/verifikator/', views.list_user_verifikator, name='list_user_verifikator'),
    path('edit/user/verifikator/<int:pk>/', views.edit_user_verifikator, name='edit_user_verifikator'),

    path('list/pengaturan/sla', views.list_pengaturan_sla, name='list_pengaturan_sla'),
    path('add/pengaturan/sla', views.add_pengaturan_sla, name='add_pengaturan_sla'),
    path('edit/pengaturan/sla/<int:pk>', views.edit_pengaturan_sla, name='edit_pengaturan_sla'),

    # download
    path('download/cbg/', views.download_data_cbg, name='download_data_cbg'),
    path('download/obat/', views.download_data_obat, name='download_data_obat'),

    # pembagian null
    path('pembagian-verifikator-cbg-null/', views.pembagian_verifikator_cbg_null, name='pembagian_verifikator_cbg_null')

]
