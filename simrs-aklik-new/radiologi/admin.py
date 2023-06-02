from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    KategoriLayananRadiologi,
    LayananRadiologi,
    LayananRadiologiPasien,
    FileTracer
)


@admin.register(KategoriLayananRadiologi)
class KategoriLayananRadiologiAdmin(admin.ModelAdmin):
    pass


class LayananRadiologiAdmin(ImportExportModelAdmin):
    list_display = (
        'nama', 'harga', 'created_at')
    search_fields = ('nama', 'harga')


admin.site.register(LayananRadiologi, LayananRadiologiAdmin)


class LayananRadiologiPasienAdmin(ImportExportModelAdmin):
    list_display = (
        'diagnosa', 'harga', 'kuantitas', 'total_harga', 'status_pembayaran', 'status_layanan', 'created_at')
    search_fields = ('diagnosa', 'status_layanan')


admin.site.register(LayananRadiologiPasien, LayananRadiologiPasienAdmin)

@admin.register(FileTracer)
class FileTracerAdmin(admin.ModelAdmin):
    pass