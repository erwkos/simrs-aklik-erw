from django.contrib import admin

from .models import (
    ICD10,
    ICD9
)


@admin.register(ICD10)
class ICDXAdmin(admin.ModelAdmin):
    pass


@admin.register(ICD9)
class ICD9Admin(admin.ModelAdmin):
    pass
