from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views, api_views
from .cekgroupingfix import query_icd10, query_icd9, grouping
from .views import cek_grouping, is_bayi

router = SimpleRouter(trailing_slash=False)
router.register('api/register/', api_views.RegisterPostKlaimViewSet, basename='api-register-vpkaak')
router.register('api/register/supervisorkp', api_views.RegisterPostKlaimSupervisorKPViewSet, basename='api-register-vpkaak-supervisorkp')


urlpatterns = [
    path('register', views.register_post_klaim, name='register-post-klaim'),
    path('import-sampling-data-klaim', views.import_sampling_data_klaim, name='import-sampling-data-klaim'),
    path('review/post-klaim', views.review, name='review-post-klaim'),
    path('update/review/<int:pk>', views.update_review, name='update-review'),
    path('finalisasi/register/post-klaim', views.finalisasi_register_post_klaim, name='finalisasi-register-post-klaim'),
    path('update/finalisasi/register/post-klaim/<int:pk>', views.update_finalisasi_register_post_klaim, name='update-finalisasi-register-post-klaim'),
    path('kertas-kerja-verifikasi', views.kertas_kerja_koreksi, name='kertas-kerja-koreksi'),
    path('input-nomor-ba/<int:pk>', views.input_nomor_ba, name='input-nomor-ba'),

    # review dari data kp
    path('review/post-klaim/kp', views.reviewkp, name='review_post_klaim_kp'),

    # grouping
    path('query_icd10/', query_icd10, name='query_icd10'),
    path('query_icd9/', query_icd9, name='query_icd9'),
    path('cek_grouping/', cek_grouping, name='cek_grouping'),
    path('is_bayi/', is_bayi, name='is_bayi'),
    # supervisorkp
    path('register/supervisorkp', views.register_post_klaim_supervisorkp, name='register_post_klaim_supervisorkp'),
    path('import-sampling-data-klaim/supervisorkp', views.import_sampling_data_klaim_supervisorkp, name='import_sampling_data_klaim_supervisorkp'),


] + router.urls
