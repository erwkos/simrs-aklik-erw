from django.contrib import admin
#
# from antrian.models import Loket, Antrian
#
# # Register your models here.
# admin.site.register(Loket)
# admin.site.register(Antrian)

from .models import Antrian


@admin.register(Antrian)
class AntrianAdmin(admin.ModelAdmin):
    pass