from django.db import models

from user.models import User
from icd.models import ICD9, ICD10
from .choices import (
    StatusPembayaranChoices,
    KondisiUmumChoices,
    KesadaranChoices,
    IsiChoices,
    StatusGeneralisChoices,
    KeadaanKeluarChoices,
    CaraKeluarChoices,
    PemeriksaanLanjutan,
    StatusPembayaranChoices
)

from kasir.models import SummaryInvoice


class Poli(models.Model):
    nama = models.CharField(max_length=150)
    harga = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class InvoicePoliPasien(models.Model):
    resume_medis = models.ForeignKey('pasien.ResumeMedis', on_delete=models.SET_NULL, blank=True, null=True)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    total_harga = models.FloatField(default=0)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices, default=StatusPembayaranChoices.BELUM_BAYAR)
    poli = models.ForeignKey(Poli, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



# class KondisiPasien(models.Model):
#     antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
#     dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='kondisi_dokter')
#     perawat = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='kondisi_perawat')
#
#     #   Kondisi -> subject
#     keluhan_utama = models.TextField(null=True, blank=True)
#     kondisi_umum = models.CharField(max_length=100, choices=KondisiUmumChoices.choices)
#     riwayat_penyakit_dahulu = models.TextField(null=True, blank=True)
#     riwayat_penyakit_sekarang = models.TextField(null=True, blank=True)
#
#     #   Tanda vital - object
#     kesadaran = models.CharField(max_length=100, choices=KesadaranChoices.choices)
#     tensi_sistol = models.CharField(max_length=50, null=True, blank=True)
#     tensi_diastol = models.CharField(max_length=50, null=True, blank=True)
#     nadi = models.CharField(max_length=50, null=True, blank=True)
#     isi = models.CharField(max_length=100, choices=IsiChoices.choices, default=IsiChoices.CUKUP)
#     rr = models.CharField(max_length=50, null=True, blank=True)
#     suhu = models.CharField(max_length=50, null=True, blank=True)
#     down_score = models.CharField(max_length=50, null=True, blank=True)
#     trauma_score = models.CharField(max_length=50, null=True, blank=True)
#     meows_score = models.CharField(max_length=50, null=True, blank=True)
#     berat_badan = models.CharField(max_length=50, null=True, blank=True)
#     tinggi_badan = models.CharField(max_length=50, null=True, blank=True)
#     gcs_e = models.CharField(max_length=50, null=True, blank=True)
#     gcs_m = models.CharField(max_length=50, null=True, blank=True)
#     gcs_v = models.CharField(max_length=50, null=True, blank=True)
#
#     #   Status generalis - object
#     kepala = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     mata = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     telinga = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     hidung = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     gigi = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     mulut = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     leher = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     wajah = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     thorax = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     paru_paru = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     jantung = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     abdomen = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     hati = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     limpa = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     generalia = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices, default=StatusGeneralisChoices.NORMAL)
#     ekstrimitas = models.TextField(null=True, blank=True)
#     status_lokalis = models.TextField(null=True, blank=True)
#
#     #   Tata laksana - planning
#     rencana_tindakan = models.TextField(null=True, blank=True)
#     terapi_obat_obatan = models.TextField(null=True, blank=True)
#     rencana_konsultasi = models.TextField(null=True, blank=True)
#
#     #   Discharge planning - > planing
#     rencana_rawat = models.CharField(max_length=10, null=True, blank=True)  # Dalam hari
#     rencana_perawatan_pasca_rawat = models.CharField(max_length=150, null=True, blank=True)
#
#     #   Keluar
#     keadaan_keluar = models.CharField(max_length=50, choices=KeadaanKeluarChoices.choices, blank=True, null=True)
#     cara_keluar = models.CharField(max_length=50, choices=CaraKeluarChoices.choices, blank=True, null=True)
#     pemeriksaan_lanjutan = models.CharField(max_length=50, choices=PemeriksaanLanjutan.choices, blank=True, null=True)


