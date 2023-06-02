from django.urls import path

from . import views


urlpatterns = [
    path('<int:pk>', views.SOAPRawatJalanView.as_view()),
    path('subjective', views.SubjectiveRawatJalanView.as_view()),
    path('objective', views.ObjectiveRawatJalanView.as_view()),
    path('planning', views.PlanningRawatJalanView.as_view()),
    path('assessment-icd10', views.AssessmentICD10RawatJalanView.as_view()),
    path('assessment-icd10/<int:pk>/hapus', views.HapusAssessmentICD10.as_view()),
    path('assessment-icd9', views.AssessmentICD9RawatJalanView.as_view()),
    path('assessment-icd9/<int:pk>/hapus', views.HapusAssessmentICD9.as_view()),



    #   rawat inap
    path('rawat-inap', views.RawatInapView.as_view())
]
