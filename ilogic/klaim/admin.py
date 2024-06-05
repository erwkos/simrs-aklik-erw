from functools import reduce

from django.contrib import admin
from .models import (
    JenisKlaim,
    RegisterKlaim,
    DataKlaimCBG, SLA, KeteranganPendingDispute, DataKlaimObat, JawabanPendingDispute
)

from operator import or_
from django.db.models import Q

from import_export.admin import ImportExportModelAdmin


@admin.register(RegisterKlaim)
class RegisterKlaimAdmin(ImportExportModelAdmin):
    search_fields = ['nomor_register_klaim']


@admin.register(JenisKlaim)
class JenisKlaimAdmin(admin.ModelAdmin):
    pass


# @admin.register(DataKlaim)
# class DataKlaimAdmin(admin.ModelAdmin):
#     pass


@admin.register(DataKlaimCBG)
class DataKlaimCBGAdmin(ImportExportModelAdmin):
    search_fields = ('NOSEP', 'register_klaim__nomor_register_klaim',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(DataKlaimCBGAdmin, self).get_search_results(
            request, queryset, search_term)
        search_words = search_term.split()
        if search_words:
            q_objects = [Q(**{field + '__icontains': word})
                         for field in self.search_fields
                         for word in search_words]
            queryset |= self.model.objects.filter(reduce(or_, q_objects))
        return queryset, use_distinct


@admin.register(DataKlaimObat)
class DataKlaimObatAdmin(ImportExportModelAdmin):
    search_fields = ('NoSEPApotek', 'NoSEPAsalResep', 'register_klaim__nomor_register_klaim')


@admin.register(SLA)
class SLAAdmin(ImportExportModelAdmin):
    search_fields = ('jenis_klaim__nama',)


@admin.register(KeteranganPendingDispute)
class KeteranganPendingDisputeAdmin(ImportExportModelAdmin):
    search_fields = ('ket_pending_dispute',)


@admin.register(JawabanPendingDispute)
class JawabanPendingDisputeAdmin(ImportExportModelAdmin):
    search_fields = ('ket_jawaban_pending',)
