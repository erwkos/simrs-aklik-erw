from django.contrib import admin

from .models import DataPerawat


@admin.register(DataPerawat)
class DataPerawatAdmin(admin.ModelAdmin):
    pass
