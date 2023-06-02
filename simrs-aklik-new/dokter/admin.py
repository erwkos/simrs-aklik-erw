from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import DataDokter


class DataDokterAdmin(ImportExportModelAdmin):
    pass
    # list_display = (
    #     'sip')
    # search_fields = ('hasil', 'created_at')


admin.site.register(DataDokter, DataDokterAdmin)
