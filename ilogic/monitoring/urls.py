from django.urls import path
from . import views


urlpatterns = [
    # cbg
    path('api/json/monitoring/dataklaim/CBG', views.api_json_data_klaim_CBG, name='api_json_data_klaim_CBG'),
    path('api/json/monitoring/dataklaim/verifikator/CBG', views.api_json_data_klaim_CBG_verifikator, name='api_json_data_klaim_CBG_verifikator'),
    path('api/json/monitoring/dataklaim/supervisor/CBG', views.api_json_data_klaim_CBG_supervisor, name='api_json_data_klaim_CBG_supervisor'),
    path('api/json/monitoring/dataklaim/CBG/stafak', views.api_json_data_klaim_CBG_stafak, name='api_json_data_klaim_CBG_stafak'),

    path('dataklaim/CBG', views.monitoring_data_klaim_CBG, name='monitoring_data_klaim_CBG'),
    path('dataklaim/CBG/verifikator', views.monitoring_data_klaim_CBG_verifikator, name='monitoring_data_klaim_CBG_verifikator'),
    path('dataklaim/CBG/supervisor', views.monitoring_data_klaim_CBG_supervisor, name='monitoring_data_klaim_CBG_supervisor'),
    path('dataklaim/CBG/stafak', views.monitoring_data_klaim_CBG_stafak, name='monitoring_data_klaim_CBG_stafak'),

    # obat
    path('api/json/monitoring/dataklaim/obat/verifikator', views.api_json_data_klaim_obat_verifikator, name='api_json_data_klaim_obat_verifikator'),
    path('api/json/monitoring/dataklaim/obat/stafak', views.api_json_data_klaim_obat_stafak, name='api_json_data_klaim_obat_stafak'),
    path('api/json/monitoring/dataklaim/obat/supervisor', views.api_json_data_klaim_obat_supervisor, name='api_json_data_klaim_obat_supervisor'),

    path('dataklaim/obat/verifikator/', views.monitoring_data_klaim_obat_verifikator,name='monitoring_data_klaim_obat_verifikator'),
    path('dataklaim/obat/stafak/', views.monitoring_data_klaim_obat_stafak, name='monitoring_data_klaim_obat_stafak'),
    path('dataklaim/obat/supervisor/', views.monitoring_data_klaim_obat_supervisor, name='monitoring_data_klaim_obat_supervisor'),

    # pending/dispute
    path('api/json/monitoring/dataklaim/cbg/pending/dispute', views.api_json_data_klaim_pending_dispute_CBG, name='api_json_data_klaim_pending_dispute_CBG'),
    path('api/json/monitoring/dataklaim/cbg/pending/dispute/stafak', views.api_json_data_klaim_pending_dispute_CBG_stafak, name='api_json_data_klaim_pending_dispute_CBG_stafak'),
    path('api/json/monitoring/dataklaim/obat/pending/dispute/verifikator', views.api_json_data_klaim_pending_dispute_obat_verifikator, name='api_json_data_klaim_pending_dispute_obat_verifikator'),
    path('api/json/monitoring/dataklaim/obat/pending/dispute/stafak', views.api_json_data_klaim_pending_dispute_obat_stafak, name='api_json_data_klaim_pending_dispute_obat_stafak'),

    path('dataklaim/CBG/pending/dispute', views.monitoring_data_klaim_pending_dispute_CBG, name='monitoring_data_klaim_pending_dispute_CBG'),
    path('dataklaim/CBG/pending/dispute/stafak', views.monitoring_data_klaim_pending_dispute_CBG_stafak, name='monitoring_data_klaim_pending_dispute_CBG_stafak'),
    path('dataklaim/obat/pending/dispute/verifikator', views.monitoring_data_klaim_pending_dispute_obat_verifikator, name='monitoring_data_klaim_pending_dispute_obat_verifikator'),
    path('dataklaim/obat/pending/dispute/stafak', views.monitoring_data_klaim_pending_dispute_obat_stafak, name='monitoring_data_klaim_pending_dispute_obat_stafak'),

    # hitung
    path('api/json/monitoring/dataklaim/hitung/verifikator', views.api_json_data_klaim_hitung_verifikator, name='api_json_data_klaim_hitung_verifikator'),
    path('api/json/monitoring/dataklaim/hitung/supervisor', views.api_json_data_klaim_hitung_supervisor, name='api_json_data_klaim_hitung_supervisor'),

    path('dataklaim/hitung/verifikator', views.monitoring_data_klaim_hitung_verifikator, name='monitoring_data_klaim_hitung_verifikator'),
    path('dataklaim/hitung/supervisor', views.monitoring_data_klaim_hitung_supervisor, name='monitoring_data_klaim_hitung_supervisor'),

]