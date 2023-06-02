from django.contrib import admin

from .models import (
    Pendaftaran,
    Pasien
)




@admin.register(Pendaftaran)
class PendafatarnAdmin(admin.ModelAdmin):
    pass


@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    pass





