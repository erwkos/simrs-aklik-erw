from django.db import models

import uuid

from user.models import User
# .............................
# task_id 1 Waktu tunggu admisi
# task_id 2 Mulai layanan admisi
# task_id 3 Tunggu poli
# task_id 4 Mulai layanan poli
# task_id 4.5 Tunggu kasir
# task_id 4.8 Mulai Kasir
# task_id 5 Waktu tunggu farmasi
# task_id 6 Mulai Membuat obat
# task_id 7 Waktu akhir membuat obat
# task_id 99 Tidak hadir/batal


class Loket(models.Model):
    kode = models.UUIDField(blank=True, null=True, default=uuid.uuid4)
    nama = models.CharField(max_length=100)
    loket = models.CharField(max_length=255, null=True, blank=True)
    petugas_admisi = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='loket_petugas_admisi')
    created_at = models.DateTimeField(auto_now_add=True)


class Antrian(models.Model):
    no_antrian = models.IntegerField()
    tanggal_periksa = models.DateField()
    waktu_start_mengantri = models.DateTimeField(auto_now_add=True)
    waktu_end_mengantri = models.DateTimeField(null=True, blank=True)
    waktu_start_layanan = models.DateTimeField(null=True, blank=True)
    waktu_end_layanan = models.DateTimeField(null=True, blank=True)
    task_id = models.FloatField(default=1)
    antrian_tanggal = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    loket = models.ForeignKey(Loket, on_delete=models.SET_NULL, blank=True, null=True)

    @classmethod
    def generate_no_antrian(cls, tanggal_periksa):
        antrian = cls.objects.filter(tanggal_periksa=tanggal_periksa)
        if antrian.exists():
            last_no_antrian = int(antrian.last().no_antrian)
        else:
            last_no_antrian = 0
        new_no_antrian = last_no_antrian + 1
        return new_no_antrian

