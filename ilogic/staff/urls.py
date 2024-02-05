from django.urls import path

from . import views

urlpatterns = [
    path('register/daftar', views.daftar_register_klaim, name='daftar-register'),
    path('register/detail/<int:pk>', views.detail_register, name='detail-register'),
    path('list/user/verifikator/', views.list_user_verifikator, name='list_user_verifikator'),
    path('edit/user/verifikator/<int:pk>/', views.edit_user_verifikator, name='edit_user_verifikator'),
    path('ambil/nosep/cbg', views.ambil_nosep_cbg, name='ambil_nosep_cbg'),
    path('register/boa/daftar', views.daftar_proses_boa, name='daftar_proses_boa'),
    path('register/boa/edit/<int:pk>', views.edit_proses_boa, name='edit_proses_boa'),
]
