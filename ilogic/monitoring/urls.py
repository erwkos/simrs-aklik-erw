from django.urls import path
from . import views


urlpatterns = [
    path('api/json/monitoring/dataklaim/CBG/', views.api_json_data_klaim_CBG, name='api_json_data_klaim_CBG'),
    path('api/json/monitoring/dataklaim/verifikator/CBG/', views.api_json_data_klaim_CBG_verifikator, name='api_json_data_klaim_CBG_verifikator'),
    path('api/json/monitoring/dataklaim/supervisor/CBG/', views.api_json_data_klaim_CBG_supervisor, name='api_json_data_klaim_CBG_supervisor'),
    path('api/json/monitoring/dataklaim/hitung/verifikator/', views.api_json_data_klaim_hitung_verifikator, name='api_json_data_klaim_hitung_verifikator'),
    path('api/json/monitoring/dataklaim/hitung/supervisor/', views.api_json_data_klaim_hitung_supervisor, name='api_json_data_klaim_hitung_supervisor'),
    path('api/json/monitoring/dataklaim/pending/dispute/', views.api_json_data_klaim_pending_dispute_CBG, name='api_json_data_klaim_pending_dispute_CBG'),
    path('dataklaim/CBG/', views.monitoring_data_klaim_CBG, name='monitoring_data_klaim_CBG'),
    path('dataklaim/CBG/verifikator/', views.monitoring_data_klaim_CBG_verifikator, name='monitoring_data_klaim_CBG_verifikator'),
    path('dataklaim/CBG/supervisor/', views.monitoring_data_klaim_CBG_supervisor, name='monitoring_data_klaim_CBG_supervisor'),
    path('dataklaim/hitung/verifikator/', views.monitoring_data_klaim_hitung_verifikator, name='monitoring_data_klaim_hitung_verifikator'),
    path('dataklaim/hitung/supervisor/', views.monitoring_data_klaim_hitung_supervisor, name='monitoring_data_klaim_hitung_supervisor'),
    path('dataklaim/CBG/pending/dispute/', views.monitoring_data_klaim_pending_dispute_CBG, name='monitoring_data_klaim_pending_dispute_CBG'),

]