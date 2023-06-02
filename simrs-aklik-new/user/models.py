from django.db import models
from django.contrib.auth.models import AbstractUser

from .choices import (
    GenderChoices
)


class UserRole(models.Model):
    nama = models.CharField(max_length=100)
    keterangan = models.TextField()

    def __str__(self):
        return self.nama


class User(AbstractUser):
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, blank=True, null=True)
    id_number = models.CharField(max_length=20, null=True, blank=True)
    nama_depan = models.CharField(max_length=255)
    nama_belakang = models.CharField(max_length=255, null=True, blank=True)
    nip = models.CharField(max_length=20, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=10, choices=GenderChoices.choices)
    tanggal_lahir = models.DateField(null=True, blank=True)
    agama = models.CharField(max_length=50, null=True, blank=True)
    no_kartu_keluarga = models.CharField(max_length=20, null=True, blank=True)
    posisi_di_keluarga = models.CharField(max_length=50, null=True, blank=True)
    pendidikan_terakhir = models.CharField(max_length=255, null=True, blank=True)
    profesi = models.CharField(max_length=255, null=True, blank=True)
    pekerjaan = models.CharField(max_length=255, null=True, blank=True)
    no_npwp = models.CharField(max_length=20, null=True, blank=True)
    sip = models.CharField(max_length=20, null=True, blank=True)    # Surat Izin Praktik
    nama_ibu_kandung = models.CharField(max_length=255, null=True, blank=True)
    golongan = models.CharField(max_length=50, null=True, blank=True)   # ex: karyawan gol 1, gol 2
    pangkat = models.CharField(max_length=50, null=True, blank=True)    # ex: direktur
    status_karyawan = models.CharField(max_length=50, null=True, blank=True)    # ex: kontrak, tetap
    unit_kerja = models.CharField(max_length=255, null=True, blank=True)    #
    no_sk_pengangkatan = models.CharField(max_length=20, null=True, blank=True)
    tanggal_sk_pengangkatan = models.DateField(null=True, blank=True)
    tanggal_masuk_rs = models.DateField(null=True, blank=True)
    no_telepon = models.CharField(max_length=15, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    alamat_kelurahan = models.CharField(max_length=255, null=True, blank=True)
    alamat_kecamatan = models.CharField(max_length=255, null=True, blank=True)
    alamat_kabupaten_kota = models.CharField(max_length=255, null=True, blank=True)
    alamat_provinsi = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

