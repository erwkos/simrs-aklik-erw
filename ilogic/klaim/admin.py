from django.contrib import admin
from .models import (
    JenisKlaim,
    RegisterKlaim,
    DataKlaimCBG, SLA, KeteranganPendingDispute, DataKlaimObat
)

from import_export.admin import ImportExportModelAdmin

@admin.register(RegisterKlaim)
class RegisterKlaimAdmin(ImportExportModelAdmin):
    search_fields = ['nomor_register_klaim']


@admin.register(JenisKlaim)
class JenisKlaimAdmin(admin.ModelAdmin):
    pass


# @admin.register(DataKlaim)
# class DataKlaimAdmin(admin.ModelAdmin):
#     pass


@admin.register(DataKlaimCBG)
class DataKlaimCBGAdmin(ImportExportModelAdmin):
    search_fields = ('NOSEP',)


@admin.register(DataKlaimObat)
class DataKlaimObatAdmin(ImportExportModelAdmin):
    search_fields = ('NoSEPApotek', 'NoSEPAsalResep',)


@admin.register(SLA)
class SLAAdmin(ImportExportModelAdmin):
    search_fields = ('jenis_klaim__nama',)


@admin.register(KeteranganPendingDispute)
class KeteranganPendingDisputeAdmin(ImportExportModelAdmin):
    search_fields = ('verifikator', )