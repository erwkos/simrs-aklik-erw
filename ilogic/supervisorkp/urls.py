from django.urls import path
from . import views

urlpatterns = [
    path('api/json/monitoring/register/', views.api_json_register_supervisorkp, name='api_json_register_supervisorkp'),
    path('monitoring/register/', views.monitoring_register_supervisorkp, name='monitoring_register_supervisorkp'),
    path('manajemen/daftar/user/', views.daftar_user_supervisorkp, name='daftar_user_supervisorkp'),
    path('manajemen/edit/user/<int:pk>/', views.update_user_supervisorkp, name='update_user_supervisorkp'),
    path('manajemen/edit/<int:pk>/password/', views.reset_password_supervisorkp, name='reset_password_supervisorkp'),
    path('manajemen/add/user/', views.add_user_supervisorkp, name='add_user_supervisorkp'),
    path('data/klaim/cbg/', views.daftar_data_klaim_cbg, name='daftar_data_klaim_cbg'),
]