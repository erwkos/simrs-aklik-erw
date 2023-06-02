from django.contrib.auth.decorators import login_required
from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

# router = SimpleRouter(trailing_slash=False)
# router.register('dashboard', views.DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('dashboard', views.dashboard),
    path('profil', views.profil),
]
