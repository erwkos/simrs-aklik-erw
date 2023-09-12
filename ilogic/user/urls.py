from django.urls import include, path

from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('ubahpassword', views.ubahpassword, name='ubahpassword'),
    path('logout', views.user_logout, name='logout'),

    path('new-user/', views.create_user_kantor_cabang, name='web_usr_add'),
    path('kanca/', include([
        path('user/change/group/<pk>/', views.change_group, name='kanca_grp_change'),
        path('user/group/add/kantorcabang', views.add_group, name='kanca_grp_add'),
        path('user/change/password/<pk>/', views.change_password, name='kanca_usr_passwd'),
        path('', views.user_per_kanca, name='kanca_user_list')
    ])),

    path('faskes/', include([
        path('', views.user_per_faskes, name='cbg_user_list')
    ])),

    path('new-user/faskes/', views.create_user_faskes, name='create_user_faskes'),

    path('list/verifikator/', views.user_per_verifikator, name='user_per_verifikator'),
    path('edit/active/verifikator/<int:pk>/', views.edit_user_verifikator_active, name='edit_user_verifikator_active'),
    path('edit/staff/verifikator/<int:pk>/', views.edit_user_verifikator_staff, name='edit_user_verifikator_staff'),
]
