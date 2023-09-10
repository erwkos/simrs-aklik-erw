from django.urls import path

from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('daftar-register', views.daftar_register, name='daftar-register'),
    path('detail-register/<int:pk>', views.detail_register, name='detail-register'),
    path('daftar/dataklaim/pending/dispute/', views.daftar_data_klaim_pending_dispute_cbg,
         name='daftar_data_klaim_pending_dispute_cbg'),
    path('detail/dataklaim/pending/dispute/<int:pk>/', views.detail_data_klaim_pending_dispute_cbg,
         name='detail_data_klaim_pending_dispute_cbg'),

]
