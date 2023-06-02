from django.db import models

import time

from user.models import User
from .choices import (
    StatusPembayaranChoices
)
from antrian.models import Antrian


class PetugasKasir(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SummaryInvoice(models.Model):
    kode_invoice = models.CharField(max_length=100, unique=True)
    resume_medis = models.CharField(max_length=100, blank=True, null=True)
    antrian = models.ForeignKey(Antrian, on_delete=models.SET_NULL, blank=True, null=True)
    petugas_kasir = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    totals = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_kode_invoice(cls):
        current_time = int(round(time.time() * 1000))
        kode = f'INV-{current_time}'
        if cls.objects.filter(kode_invoice=kode):
            return cls.generate_kode_invoice()
        return kode

