from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views, api_views

router = SimpleRouter(trailing_slash=False)
router.register('api/register/', api_views.RegisterPostKlaimViewSet, basename='api-register-vpkaak')


urlpatterns = [
    path('register', views.register_post_klaim, name='register-post-klaim'),
    path('import-sampling-data-klaim', views.import_sampling_data_klaim, name='import-sampling-data-klaim'),
    path('review/post-klaim', views.review, name='review-post-klaim'),
    path('update/review/<int:pk>', views.update_review, name='update-review'),
    path('finalisasi/register/post-klaim', views.finalisasi_register_post_klaim, name='finalisasi-register-post-klaim'),
    path('update/finalisasi/register/post-klaim/<int:pk>', views.update_finalisasi_register_post_klaim, name='update-finalisasi-register-post-klaim'),
    path('kertas-kerja-verifikasi', views.kertas_kerja_koreksi, name='kertas-kerja-koreksi'),
    path('input-nomor-ba/<int:pk>', views.input_nomor_ba, name='input-nomor-ba'),

    # supervisorkp
    path('register/supervisorkp', views.register_post_klaim_supervisorkp, name='register_post_klaim_supervisorkp'),


] + router.urls
