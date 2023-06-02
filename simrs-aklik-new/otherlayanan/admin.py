from django.contrib import admin


from .models import (
    LayananTindakan,
    LayananKonsultasi,
    LayananMonitoring,
    LayananEdukasi,

    LayananEdukasiPasien,
    LayananTindakanPasien,
    LayananKonsultasiPasien,
    LayananMonitoringPasien
)


@admin.register(LayananTindakan)
class LayananTindakanAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananKonsultasi)
class LayananKonsultasiAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananMonitoring)
class LayananMonitoringAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananEdukasi)
class LayananEdukasiAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananEdukasiPasien)
class LayananEdukasiPasienAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananTindakanPasien)
class LayananTindakanPasienAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananKonsultasiPasien)
class LayananKonsultasiPasienAdmin(admin.ModelAdmin):
    pass


@admin.register(LayananMonitoringPasien)
class LayananMonitoringPasienAdmin(admin.ModelAdmin):
    pass
