from django.urls import path
from . import views

urlpatterns = [
    path('list/noba/kp', views.list_no_ba_cbg_metafisik_kp, name='list_no_ba_cbg_metafisik_kp'),
    path('list/noba', views.list_no_ba_cbg_metafisik, name='list_no_ba_cbg_metafisik'),
    path('import/noba', views.import_no_ba_cbg_metafisik, name='import_no_ba_cbg_metafisik'),
    path('import/data-klaim', views.import_data_klaim_cbg_metafisik, name='import_data_klaim_cbg_metafisik'),
]