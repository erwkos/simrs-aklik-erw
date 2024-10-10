from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from metafisik.models import NoBAMetafisik, DataKlaimCBGMetafisik


# Register your models here.
@admin.register(NoBAMetafisik)
class NoBAMetafisikAdmin(ImportExportModelAdmin):
    search_fields = ['no_surat_bast', 'kdkrlayan', 'kdkclayan', 'kdppklayan', 'nmppklayan', 'tgl_bast']


@admin.register(DataKlaimCBGMetafisik)
class DataKlaimCBGMetafisikAdmin(ImportExportModelAdmin):
    search_fields = ['no_bast__no_surat_bast', 'nosjp', 'no_bast__tgl_bast']
    list_filter = [
        ('no_bast__tgl_bast', admin.DateFieldListFilter),
    ]
