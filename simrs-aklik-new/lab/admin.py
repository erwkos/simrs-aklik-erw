from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    LayananLab,
    SubLayananLab,
    LayananLabPasien,
    HasilSubLayananLab,
    KategoriLayananLab
)


class KategoriLayananLabAdmin(ImportExportModelAdmin):
    list_display = (
        'nama', 'created_at')
    search_fields = ('nama', 'created_at')


admin.site.register(KategoriLayananLab, KategoriLayananLabAdmin)


class LayananLabAdmin(ImportExportModelAdmin):
    list_display = (
        'nama', 'harga', 'created_at')
    search_fields = ('nama', 'harga')


admin.site.register(LayananLab, LayananLabAdmin)


class LayananLabPasienAdmin(ImportExportModelAdmin):
    list_display = (
        'diagnosa', 'harga', 'kuantitas', 'total_harga', 'status_pembayaran', 'status_layanan', 'created_at')
    search_fields = ('diagnosa', 'status_layanan')


admin.site.register(LayananLabPasien, LayananLabPasienAdmin)


class SubLayananLabAdmin(ImportExportModelAdmin):
    list_display = (
        'nama', 'hasil_normal', 'created_at')
    search_fields = ('nama', 'hasil_normal')


admin.site.register(SubLayananLab, SubLayananLabAdmin)


class HasilSubLayananLabAdmin(ImportExportModelAdmin):
    list_display = (
        'hasil', 'created_at')
    search_fields = ('hasil', 'created_at')


admin.site.register(HasilSubLayananLab, HasilSubLayananLabAdmin)
