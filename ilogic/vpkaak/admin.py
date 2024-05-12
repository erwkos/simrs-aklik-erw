from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from vpkaak.models import RegisterPostKlaim, SamplingDataKlaimCBG


# Register your models here.
@admin.register(RegisterPostKlaim)
class RegisterPostKlaimAdmin(ImportExportModelAdmin):
    search_fields = ('nomor_register',)


# admin.site.register(RegisterPostKlaim)
admin.site.register(SamplingDataKlaimCBG)
