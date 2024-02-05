from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from dokumentasi.models import PolaRules, ProgressVersion


@admin.register(PolaRules)
class PolaRulesAdmin(ImportExportModelAdmin):
    search_fields = ('nama_rules',)


@admin.register(ProgressVersion)
class ProgressVersionAdmin(ImportExportModelAdmin):
    search_fields = ('version',)
