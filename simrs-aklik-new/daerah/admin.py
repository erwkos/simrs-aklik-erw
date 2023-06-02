from django.contrib import admin

from .models import (
    Provinsi,
    Kabupaten,
    Kecamatan,
    Daerah
)



@admin.register(Provinsi)
class ProvinsiAdmin(admin.ModelAdmin):
    pass


@admin.register(Kabupaten)
class KabupatenAdmin(admin.ModelAdmin):
    pass


@admin.register(Kecamatan)
class KecamatanAdmin(admin.ModelAdmin):
    pass


@admin.register(Daerah)
class DaerahAdmin(admin.ModelAdmin):
    pass
