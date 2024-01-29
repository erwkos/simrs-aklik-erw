from django.urls import path
from . import views

urlpatterns = [
    path('api/json/monitoring/register/', views.api_json_register_supervisorkp, name='api_json_register_supervisorkp'),
    path('monitoring/register/', views.monitoring_register_supervisorkp, name='monitoring_register_supervisorkp'),
]