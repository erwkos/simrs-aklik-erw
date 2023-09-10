from django.urls import path

from . import views

urlpatterns = [
    path('register/daftar', views.daftar_register_klaim, name='daftar-register'),
    path('register/detail/<int:pk>', views.detail_register, name='detail-register'),
    path('list/user/verifikator/', views.list_user_verifikator, name='list_user_verifikator'),
    path('edit/user/verifikator/<int:pk>/', views.edit_user_verifikator, name='edit_user_verifikator'),
    # path('monitoring/data-klaim', views.monitoring_data_klaim, name='monitoring-data-klaim')
]
