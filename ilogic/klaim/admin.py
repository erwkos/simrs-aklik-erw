from django.contrib import admin
from .models import (
    JenisKlaim,
    RegisterKlaim,
    DataKlaimCBG
)

from import_export.admin import ImportExportModelAdmin

@admin.register(RegisterKlaim)
class RegisterKlaimAdmin(admin.ModelAdmin):
    pass


@admin.register(JenisKlaim)
class JenisKlaimAdmin(admin.ModelAdmin):
    pass


# @admin.register(DataKlaim)
# class DataKlaimAdmin(admin.ModelAdmin):
#     pass


@admin.register(DataKlaimCBG)
class DataKlaimAdmin(ImportExportModelAdmin):
    search_fields = ('NOSEP',)
