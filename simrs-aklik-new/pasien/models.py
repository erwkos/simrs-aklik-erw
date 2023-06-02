from django.db import models

from user.models import User
from poli.models import Poli
from .choices import (
    StatusPasienChoices,
    JenisKelamin,
    TipeLayanan,
    AgamaChoices,
    StatusPembayaranChoices,
    AsuransiChoices,

    StatusLayananChoices,

    RujukanChoices,
    KeadanKeluarChoices,
    CaraKeluarChoices,
    PemeriksaanLanjutChoices
)
from antrian.models import Antrian
from kasir.models import SummaryInvoice


class Pasien(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    no_rekam_medis = models.CharField(max_length=100, unique=True)
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=100, unique=True)
    tanggal_lahir = models.DateField()
    status = models.CharField(max_length=30, choices=StatusPasienChoices.choices)
    jenis_kelamin = models.CharField(max_length=30, choices=JenisKelamin.choices)
    provinsi = models.CharField(max_length=100)
    kabupaten = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    alamat = models.CharField(max_length=100)
    agama = models.CharField(max_length=50, choices=AgamaChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

    @classmethod
    def generate_no_rekam_medis(cls):
        nrm = cls.objects.all()
        if nrm.exists():
            last = int(nrm.last().no_rekam_medis)
        else:
            last = 0
        last += 1
        new_nrm = str(last).zfill(6)
        if cls.objects.filter(no_rekam_medis=new_nrm):
            return cls.generate_no_rekam_medis()
        return new_nrm


class ResumeMedis(models.Model):
    no_resume_medis = models.CharField(max_length=100, unique=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.SET_NULL, blank=True, null=True)
    rujukan = models.CharField(max_length=50, choices=RujukanChoices.choices, blank=True, null=True)
    no_rujukan = models.CharField(max_length=100, blank=True, null=True)
    keadaan_keluar = models.CharField(max_length=100, choices=KeadanKeluarChoices.choices, blank=True, null=True)
    cara_keluar = models.CharField(max_length=100, choices=CaraKeluarChoices.choices, blank=True, null=True)
    pemeriksaan_lanjut = models.CharField(max_length=100, choices=PemeriksaanLanjutChoices.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_no_rekam_medis(cls):
        nrm = cls.objects.all()
        if nrm.exists():
            last = int(nrm.last().no_resume_medis)
        else:
            last = 0
        last += 1
        new_nrm = str(last).zfill(6)
        if cls.objects.filter(no_resume_medis=new_nrm):
            return cls.generate_no_rekam_medis()
        return new_nrm


class Pendaftaran(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
    resume_medis = models.ForeignKey(ResumeMedis, on_delete=models.SET_NULL,blank=True, null=True)
    antrian = models.OneToOneField(Antrian, on_delete=models.SET_NULL, blank=True, null=True)
    asuransi = models.CharField(max_length=30, choices=AsuransiChoices.choices, default=AsuransiChoices.UMUM)
    no_peserta = models.CharField(max_length=100, blank=True, null=True)    # nomor peserta asuransi
    tipe_layanan = models.CharField(max_length=50, choices=TipeLayanan.choices, blank=True, null=True)
    poli = models.ForeignKey(Poli, on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='pendaftaran_dokter')
    biaya = models.FloatField(default=0)
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status_layanan = models.CharField(max_length=100,
                                      choices=StatusLayananChoices.choices,
                                      default=StatusLayananChoices.BERLANGSUNG,
                                      blank=True, null=True)
    petugas = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='pendaftaran_petugas_admisi')
    created_at = models.DateTimeField(auto_now_add=True)
