"""
URL configuration for simrs_aklik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from user import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login, name="login"),
    path('postlogin', views.postlogin, name="postlogin"),
    path('logout', login_required(views.logout), name="logout"),

    path('admisi/', include(('admisi.urls', 'admisi'), namespace='admisi')),
    path('rawatinap/', include(('rawatinap.urls', 'rawatinap'), namespace='rawatinap')),
    path('pasien/', include(('pasien.urls', 'pasien'), namespace='pasien')),
    path('poli/', include(('poli.urls', 'poli'), namespace='poli')),
    path('kasir/', include(('kasir.urls', 'kasir'), namespace='kasir')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('antrian/', include('antrian.urls')),
    # path('icd/', include(('icd.urls', 'icd'), namespace='icd')),
    path('farmasi/', include(('farmasi.urls', 'farmasi'), namespace='farmasi')),
    path('radiologi/', include(('radiologi.urls', 'radiologi'), namespace='radiologi')),
    path('lab/', include(('lab.urls', 'lab'), namespace='lab')),
    path('soap/', include(('soap.urls', 'soap'), namespace='soap')),
    path('otherlayanan/', include(('otherlayanan.urls', 'otherlayanan'), namespace='otherlayanan')),
    path('dokter/', include(('dokter.urls', 'dokter'), namespace='dokter')),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),

    path('daerah/', include(('daerah.urls', 'daerah'), namespace='daerah')),
    path('igd/', include(('igd.urls', 'igd'), namespace='igd')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
