from django.db import models

from user.models import User
from pasien.models import ResumeMedis
from .choices import StatusPembayaranChoices, StatusLayananChoices
from kasir.models import SummaryInvoice


class KategoriLayananRadiologi(models.Model):
    nama = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananRadiologi(models.Model):
    nama = models.CharField(max_length=100)
    kateori = models.ForeignKey(KategoriLayananRadiologi, on_delete=models.SET_NULL, blank=True, null=True)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananRadiologiPasien(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='radiologi_dokter')
    petugas_radiologi = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='radiologi_petugas')
    layanan_radiologi = models.ForeignKey(LayananRadiologi, on_delete=models.SET_NULL, blank=True, null=True)
    harga = models.FloatField(default=0)
    kuantitas = models.IntegerField(default=1)
    total_harga = models.FloatField(default=0)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    status_layanan = models.CharField(max_length=30, choices=StatusLayananChoices.choices,
                                      default=StatusLayananChoices.MENUNGGU)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosa = models.TextField(blank=True, null=True)
    catatan = models.TextField(blank=True, null=True)


class FileTracer(models.Model):
    layanan_radiologi_pasien = models.ForeignKey(LayananRadiologiPasien, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(upload_to='radiologi/file-tracer/')
    created_at = models.DateTimeField(auto_now_add=True)



