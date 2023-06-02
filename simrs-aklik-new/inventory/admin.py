from django.contrib import admin

from .models import (
    AlatKesehatan,
    AlatKesehatanPasien
)


@admin.register(AlatKesehatan)
class AlatKesehatanAdmin(admin.ModelAdmin):
    pass


@admin.register(AlatKesehatanPasien)
class AlatKesehatanPasienAdmin(admin.ModelAdmin):
    pass
