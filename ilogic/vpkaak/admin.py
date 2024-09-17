from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from vpkaak.models import RegisterPostKlaim, SamplingDataKlaimCBG, CookiesICD


# Register your models here.
@admin.register(RegisterPostKlaim)
class RegisterPostKlaimAdmin(ImportExportModelAdmin):
    search_fields = ('nomor_register',)


@admin.register(SamplingDataKlaimCBG)
class SamplingDataKlaimCBGAdmin(ImportExportModelAdmin):
    search_fields = ('Nosjp',)


admin.site.register(CookiesICD)
