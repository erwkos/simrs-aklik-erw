import uuid

from django.contrib.auth.hashers import make_password
from django.db import models

from user.models import User


# Create your models here.
class Karyawan(models.Model):
    GENDER_CHOICES = (
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan'),
    )
    pengguna = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id_number = models.CharField(max_length=20, null=True, blank=True)
    nama_depan = models.CharField(max_length=255)
    nama_belakang = models.CharField(max_length=255, null=True, blank=True)
    nip = models.CharField(max_length=20, null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tanggal_lahir = models.DateField(null=True, blank=True)
    agama = models.CharField(max_length=50, null=True, blank=True)
    no_kartu_keluarga = models.CharField(max_length=20, null=True, blank=True)
    posisi_di_keluarga = models.CharField(max_length=50, null=True, blank=True)
    pendidikan_terakhir = models.CharField(max_length=255, null=True, blank=True)
    profesi = models.CharField(max_length=255, null=True, blank=True)
    pekerjaan = models.CharField(max_length=255, null=True, blank=True)
    no_npwp = models.CharField(max_length=20, null=True, blank=True)
    sip = models.CharField(max_length=20, null=True, blank=True)
    nama_ibu_kandung = models.CharField(max_length=255, null=True, blank=True)
    golongan = models.CharField(max_length=50, null=True, blank=True)
    pangkat = models.CharField(max_length=50, null=True, blank=True)
    status_karyawan = models.CharField(max_length=50, null=True, blank=True)
    unit_kerja = models.CharField(max_length=255, null=True, blank=True)
    no_sk_pengangkatan = models.CharField(max_length=20, null=True, blank=True)
    tanggal_sk_pengangkatan = models.DateField(null=True, blank=True)
    tanggal_masuk_rs = models.DateField(null=True, blank=True)
    no_telepon = models.CharField(max_length=15, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    alamat_kelurahan = models.CharField(max_length=255, null=True, blank=True)
    alamat_kecamatan = models.CharField(max_length=255, null=True, blank=True)
    alamat_kabupaten_kota = models.CharField(max_length=255, null=True, blank=True)
    alamat_provinsi = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Karyawan'
        verbose_name_plural = 'Data Karyawan'

    def save(self, *args, **kwargs):
        if self.pengguna is None:
            # count the total number of Pasien
            total_pasien = Karyawan.objects.count() + 1
            # pad with zeros to get 8 digits
            self.id_number = str(total_pasien).zfill(8)

            # create a new User
            self.user = User.objects.create(
                username=self.id_number,
                password=make_password("123456789"),  # agama is assumed to be a field in Pasien
            )

            self.pengguna = self.user
        super().save(*args, **kwargs)