from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Kepwil,
    KantorCabang,
    Faskes
)


@admin.register(Kepwil)
class KepwilAdmin(ImportExportModelAdmin):
    search_fields = ('nama', 'kode_kepil')


@admin.register(KantorCabang)
class KantorCabangAdmin(ImportExportModelAdmin):
    search_fields = ('nama', 'kode_cabang')


@admin.register(Faskes)
class FaskesAdmin(ImportExportModelAdmin):
    search_fields = ('nama', 'kode_ppk')
