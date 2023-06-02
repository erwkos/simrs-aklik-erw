from django.db import models

from pasien.models import ResumeMedis
from user.models import User
from kasir.models import SummaryInvoice
from .choices import (
    StatusPembayaranChoices
)


class AlatKesehatan(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.FloatField(default=0)
    stok = models.IntegerField(default=0)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama


class AlatKesehatanPasien(models.Model):
    alat = models.ForeignKey(AlatKesehatan, on_delete=models.SET_NULL, blank=True, null=True)
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    status_pembayaran = models.CharField(max_length=50, choices=StatusPembayaranChoices.choices, default=StatusPembayaranChoices.BELUM_BAYAR)
    harga = models.FloatField(default=0)
    kuantitas = models.IntegerField(default=1)
    total_harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


