from django.contrib import admin
from .models import (
    JenisKlaim,
    RegisterKlaim,
    DataKlaimCBG, SLA, KeteranganPendingDispute
)

from import_export.admin import ImportExportModelAdmin

@admin.register(RegisterKlaim)
class RegisterKlaimAdmin(admin.ModelAdmin):
    search_fields = ['nomor_register_klaim']


@admin.register(JenisKlaim)
class JenisKlaimAdmin(admin.ModelAdmin):
    pass


# @admin.register(DataKlaim)
# class DataKlaimAdmin(admin.ModelAdmin):
#     pass


@admin.register(DataKlaimCBG)
class DataKlaimAdmin(ImportExportModelAdmin):
    search_fields = ('NOSEP',)


@admin.register(SLA)
class SLAAdmin(ImportExportModelAdmin):
    search_fields = ('jenis_klaim__nama',)


@admin.register(KeteranganPendingDispute)
class KeteranganPendingDisputeAdmin(ImportExportModelAdmin):
    search_fields = ('verifikator', )