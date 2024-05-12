"""
URL configuration for viis project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from user import views
from user.views import dashboard

admin.site.site_header = "BPJS Kesehatan"
admin.site.site_title = "BPJS Kesehatan"
admin.site.index_title = "Selamat Datang di Portal BPJS Kesehatan"

admin.site.login = views.user_login

urlpatterns = [
    path('admin/ilogic/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('faskes/', include(('faskes.urls', 'faskes'), namespace='faskes')),
    path('klaim/', include(('klaim.urls', 'klaim'), namespace='klaim')),
    path('verifikator/', include(('verifikator.urls', 'verifikator'), namespace='verifikator')),
    path('staff/', include(('staff.urls', 'staff'), namespace='staff')),
    path('captcha/', include('captcha.urls')),
    path('monitoring/', include(('monitoring.urls', 'monitoring'), namespace='monitoring')),
    path('supervisor/', include(('supervisor.urls', 'supervisor'), namespace='supervisor')),
    # path('dokumentasi/', include(('dokumentasi.urls', 'dokumentasi'), namespace='dokumentasi')),
    path('supervisorkp/', include(('supervisorkp.urls', 'supervisorkp'), namespace='supervisorkp')),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
