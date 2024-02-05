from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from dokumentasi import views

from django.urls import path, include
from rest_framework import routers
from .views import PolaRulesViewSet

router = routers.DefaultRouter()
router.register(r'polarules', PolaRulesViewSet, basename='polarules')

urlpatterns = [
    path('list/pola-rules', views.list_pola_rules, name='list_pola_rules'),
    path('list/pola-rules/add', views.add_pola_rules, name='add_pola_rules'),
    path('list/pola-rules/add/same-version', views.add_pola_rules_same_version, name='add_pola_rules_same_version'),
    path('list/pola-rules/edit/open', views.open_edit_list_pola_rules, name='open_edit_list_pola_rules'),
    path('list/pola-rules/delete/<int:pk>', views.delete_pola_rules, name='delete_pola_rules'),
    path('list/pola-rules/edit/<int:pk>', views.edit_pola_rules, name='edit_pola_rules'),
    path('list/pola-rules/ajukan/<int:pk>', views.ajukan_pola_rules, name='ajukan_pola_rules'),
    path('list/pola-rules/approved/asdep/<int:pk>', views.approved_asdep_pola_rules, name='approved_asdep_pola_rules'),
    path('list/pola-rules/approved/depdirbid/<int:pk>', views.approved_depdirbid_pola_rules, name='approved_depdirbid_pola_rules'),
    path('list/pola-rules/reject', views.reject_pola_rules, name='reject_pola_rules'),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
