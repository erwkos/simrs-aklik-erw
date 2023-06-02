from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Obat, ObatPasien


class ObatAdmin(ImportExportModelAdmin):
    list_display = (
        'nama', 'kode', 'created_at')
    search_fields = ('nama', 'kode')


admin.site.register(Obat, ObatAdmin)


class ObatPasienAdmin(ImportExportModelAdmin):
    list_display = (
        'deskripsi', 'harga', 'kuantitas', 'total_harga', 'status_pembayaran', 'status_layanan', 'created_at')
    search_fields = ('deskripsi', 'status_layanan')


admin.site.register(ObatPasien, ObatPasienAdmin)
