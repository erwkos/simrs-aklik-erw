from django.db import models

from user.models import User
from pasien.models import ResumeMedis
from kasir.models import SummaryInvoice
from .choices import (
    StatusPembayaranChoices
)


class LayananEdukasi(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananMonitoring(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananTindakan(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananKonsultasi(models.Model):
    nama = models.CharField(max_length=150)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama


class LayananEdukasiPasien(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='edukasi_dokter')
    perawat = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='edukasi_perawat')
    harga = models.FloatField(default=0)
    kuantitas = models.IntegerField(default=1)
    total_harga = models.FloatField()
    layanan_edukasi = models.ForeignKey(LayananEdukasi, on_delete=models.SET_NULL, blank=True, null=True)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deskripsi = models.TextField(blank=True, null=True)


class LayananMonitoringPasien(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='monitoring_dokter')
    perawat = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='monitoring_perawat')
    harga = models.FloatField(default=0)
    kuantitas = models.IntegerField(default=1)
    total_harga = models.FloatField()
    layanan_monitoring = models.ForeignKey(LayananMonitoring, on_delete=models.SET_NULL, blank=True, null=True)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deskripsi = models.TextField(blank=True, null=True)


class LayananTindakanPasien(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='tindakan_dokter')
    perawat = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='tindakan_perawat')
    harga = models.FloatField(default=0)
    kuantitas = models.IntegerField(default=1)
    total_harga = models.FloatField()
    layanan_tindakan = models.ForeignKey(LayananTindakan, on_delete=models.SET_NULL, blank=True, null=True)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deskripsi = models.TextField(blank=True, null=True)


class LayananKonsultasiPasien(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='konsultasi_dokter')
    perawat = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='konsultasi_perawat')
    harga = models.FloatField(default=0)
    kuantitas = models.IntegerField(default=1)
    total_harga = models.FloatField()
    layanan_konsultasi = models.ForeignKey(LayananKonsultasi, on_delete=models.SET_NULL, blank=True, null=True)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deskripsi = models.TextField(blank=True, null=True)
