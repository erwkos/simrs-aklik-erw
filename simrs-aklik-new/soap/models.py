from django.db import models

from user.models import User
from icd.models import ICD9, ICD10
from pasien.models import ResumeMedis
from antrian.models import Antrian
from .choices import (
    StatusGeneralisChoices,
    KesadaranChoices,
    KondisiUmumChoices
)


class AssessmentICD10(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey('pasien.ResumeMedis', on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='icdx_dokter')
    perawat = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='icdx_perawat')
    nama = models.CharField(max_length=100, blank=True, null=True)
    kode = models.CharField(max_length=100, blank=True, null=True)
    icd10 = models.ForeignKey(ICD10, on_delete=models.SET_NULL, blank=True, null=True)


class AssessmentICD9(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey('pasien.ResumeMedis', on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='icd9_dokter')
    perawat = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='icd9_perawat')
    nama = models.CharField(max_length=100, blank=True, null=True)
    kode = models.CharField(max_length=100, blank=True, null=True)
    icd9 = models.ForeignKey(ICD9, on_delete=models.SET_NULL, blank=True, null=True)


class Subjective(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey('pasien.ResumeMedis', on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    keluhan_utama = models.TextField(null=True, blank=True)
    kondisi_umum = models.CharField(max_length=100, choices=KondisiUmumChoices.choices, null=True, blank=True)
    riwayat_penyakit_dahulu = models.TextField(null=True, blank=True)
    riwayat_penyakit_sekarang = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Objective(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey('pasien.ResumeMedis', on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    #   Tanda vital - object
    kesadaran = models.CharField(max_length=100, choices=KesadaranChoices.choices, null=True, blank=True)
    tensi_sistol = models.CharField(max_length=50, null=True, blank=True)
    tensi_diastol = models.CharField(max_length=50, null=True, blank=True)
    nadi = models.CharField(max_length=50, null=True, blank=True)
    rr = models.CharField(max_length=50, null=True, blank=True)
    suhu = models.CharField(max_length=50, null=True, blank=True)
    down_score = models.CharField(max_length=50, null=True, blank=True)
    trauma_score = models.CharField(max_length=50, null=True, blank=True)
    meows_score = models.CharField(max_length=50, null=True, blank=True)
    berat_badan = models.CharField(max_length=50, null=True, blank=True)
    tinggi_badan = models.CharField(max_length=50, null=True, blank=True)
    gcs_e = models.CharField(max_length=50, null=True, blank=True)
    gcs_m = models.CharField(max_length=50, null=True, blank=True)
    gcs_v = models.CharField(max_length=50, null=True, blank=True)

    #   Status generalis - object
    kepala = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                              default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    mata = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                            default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    telinga = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                               default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    hidung = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                              default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    gigi = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                            default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    mulut = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                             default=StatusGeneralisChoices.NORMAL)
    leher = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                             default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    wajah = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                             default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    thorax = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                              default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    paru_paru = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                                 default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    jantung = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                               default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    abdomen = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                               default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    hati = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                            default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    limpa = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                             default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    generalia = models.CharField(max_length=100, choices=StatusGeneralisChoices.choices,
                                 default=StatusGeneralisChoices.NORMAL, null=True, blank=True)
    ekstrimitas = models.TextField(null=True, blank=True)
    status_lokalis = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Planning(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey('pasien.ResumeMedis', on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    #   Tata laksana - planning
    rencana_tindakan = models.TextField(null=True, blank=True)
    terapi_obat_obatan = models.TextField(null=True, blank=True)
    rencana_konsultasi = models.TextField(null=True, blank=True)

    #   Discharge planning - > planing
    rencana_rawat = models.CharField(max_length=10, null=True, blank=True)  # Dalam hari
    rencana_perawatan_pasca_rawat = models.CharField(max_length=150, null=True, blank=True)