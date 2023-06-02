from django.db import models

from user.models import User
from .choices import StatusPembayaranChoices, StatusLayananChoices
from kasir.models import SummaryInvoice
from pasien.models import ResumeMedis


class KategoriLayananLab(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.nama


class LayananLab(models.Model):
    kategori = models.ForeignKey(KategoriLayananLab, on_delete=models.SET_NULL, blank=True, null=True)
    nama = models.CharField(max_length=100)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'layanan lab {self.nama}'


class SubLayananLab(models.Model):
    layanan_lab = models.ForeignKey(LayananLab, on_delete=models.SET_NULL, blank=True, null=True)
    nama = models.CharField(max_length=100)
    hasil_normal = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'sub layanan lab {self.layanan_lab.nama} {self.nama}'


class LayananLabPasien(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='lab_dokter')
    petugas_lab = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='lab_petugas')
    layanan_lab = models.ForeignKey(LayananLab, on_delete=models.SET_NULL, blank=True, null=True)
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

    def __str__(self):
        return f'bill {self.layanan_lab.nama}'


class HasilSubLayananLab(models.Model):
    sub_layanan_lab = models.ForeignKey(SubLayananLab, on_delete=models.SET_NULL, blank=True, null=True)
    layanan_lab_pasien = models.ForeignKey(LayananLabPasien, on_delete=models.SET_NULL, blank=True, null=True)
    hasil = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'hasil sub lab {self.sub_layanan_lab.nama}'

