from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Poli,
    InvoicePoliPasien
)


class PoliAdmin(ImportExportModelAdmin):
    list_display = (
        'nama', 'harga', 'created_at')
    search_fields = ('nama', 'harga')


admin.site.register(Poli, PoliAdmin)


@admin.register(InvoicePoliPasien)
class InvoicePoliAdmin(admin.ModelAdmin):
    pass
