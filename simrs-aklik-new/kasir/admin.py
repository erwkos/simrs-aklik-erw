from django.contrib import admin


from .models import SummaryInvoice


@admin.register(SummaryInvoice)
class SummaryInvoiceAdmin(admin.ModelAdmin):
    pass

