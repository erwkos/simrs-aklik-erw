from django.db import models

from datetime import datetime, timedelta, date

from django.utils.functional import cached_property

from faskes.models import Faskes, KantorCabang
from user.models import User
from verifikator.models import HitungDataKlaim
from .choices import (
    StatusRegisterChoices,
    JenisDisputeChoices,
    JenisPelayananChoices,
    StatusDataKlaimChoices, NamaJenisKlaimChoices, JenisPendingChoices
)
from faskes.models import (
    Faskes
)


class JenisKlaim(models.Model):
    nama = models.CharField(max_length=250, choices=NamaJenisKlaimChoices.choices, unique=True)  # penambahan choices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nama}'


class SLA(models.Model):
    jenis_klaim = models.ForeignKey(JenisKlaim, on_delete=models.CASCADE)
    kantor_cabang = models.ForeignKey(KantorCabang, on_delete=models.CASCADE)
    plus_hari_sla = models.PositiveIntegerField(default=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.jenis_klaim} - {self.kantor_cabang} - {str(self.plus_hari_sla)}'


class RegisterKlaim(models.Model):
    nomor_register_klaim = models.CharField(max_length=250, unique=True)

    faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE)
    jenis_klaim = models.ForeignKey(JenisKlaim, on_delete=models.CASCADE)
    verifikator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    status = models.CharField(max_length=50,
                              choices=StatusRegisterChoices.choices, default=StatusRegisterChoices.PENGAJUAN)

    kasus_rawat_jalan_aju = models.PositiveBigIntegerField(default=0)
    biaya_rawat_jalan_aju = models.PositiveBigIntegerField(default=0)
    kasus_rawat_inap_aju = models.PositiveBigIntegerField(default=0)
    biaya_rawat_inap_aju = models.PositiveBigIntegerField(default=0)
    # kasus_rawat_jalan_lengkap = models.IntegerField(default=0)
    # biaya_rawat_jalan_lengkap = models.BigIntegerField(default=0)
    # kasus_rawat_inap_lengkap = models.IntegerField(default=0)
    # biaya_rawat_inap_lengkap = models.BigIntegerField(default=0)
    # kasus_rawat_jalan_verifikasi = models.IntegerField(default=0)
    # biaya_rawat_jalan_verifikasi = models.BigIntegerField(default=0)
    # kasus_rawat_inap_verifikasi = models.IntegerField(default=0)
    # biaya_rawat_inap_verifikasi = models.BigIntegerField(default=0)
    bulan_pelayanan = models.DateField()

    no_ba_terima = models.CharField(max_length=25, blank=True, null=True)
    no_ba_lengkap = models.CharField(max_length=25, blank=True, null=True)
    no_ba_hasil_verifikasi = models.CharField(max_length=25, blank=True, null=True)
    tgl_terima = models.DateField(blank=True, null=True)
    tgl_ba_lengkap = models.DateField(blank=True, null=True)
    tgl_ba_verif = models.DateField(blank=True, null=True)
    keterangan = models.CharField(max_length=50, blank=True, null=True)
    absensi_klaim = models.CharField(max_length=200, blank=True, null=True)
    tgl_aju = models.DateTimeField(blank=True, null=True) # ganti jadi date time
    nomor_surat_pengajuan_rs = models.CharField(max_length=50) # default nya di hapus saja
    is_final = models.BooleanField(default=False)
    prosesboa = models.BooleanField(default=False)
    tgl_boa = models.DateField(blank=True, null=True)
    is_potongklaim = models.BooleanField(default=False)
    keterangan_potongklaim = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    file_data_klaim = models.FileField(upload_to='data-klaim/', blank=True, null=True)

    is_pengajuan_ulang = models.BooleanField(default=False)     # Flaging pengajuan ulang data klaim pending/dispute.

    # dihapus karena ada faskes dan bulan pelayanan yang bisa diajukan sama
    # class Meta:
    #     unique_together = ['faskes', 'bulan_pelayanan']

    def __str__(self):
        return f'{self.nomor_register_klaim}'

    # @property
    # def data_klaim_total(self):

    # auto tgl ba lengkap
    def save(self, *args, **kwargs):
        if self.tgl_ba_lengkap is None:
            if self.tgl_terima:
                self.tgl_ba_lengkap = self.tgl_terima + timedelta(days=9)
        elif self.tgl_ba_lengkap > self.tgl_terima + timedelta(days=9):
            self.tgl_ba_lengkap = self.tgl_terima + timedelta(days=9)
        super(RegisterKlaim, self).save(*args, **kwargs)

    @cached_property
    def tgl_hari_ini(self):
        today = date.today()
        return today

    @cached_property
    def tgl_selesai_verif(self):
        return self.tgl_ba_lengkap + timedelta(days=9)

    @cached_property
    def tgl_jatuh_tempo(self):
        return self.tgl_ba_lengkap + timedelta(days=14)

    @cached_property
    def sisa_hari(self):
        return self.tgl_selesai_verif - self.tgl_hari_ini

    @cached_property
    def tgl_ba_lengkap_seharusnya(self):
        if self.tgl_terima:
            return self.tgl_terima + timedelta(days=9)
        elif self.tgl_aju:
            return self.tgl_aju + timedelta(days=9)

    @cached_property
    def sisa_klaim(self):
        sisa_klaim = 0
        if self.jenis_klaim.nama == NamaJenisKlaimChoices.CBG_REGULER or self.jenis_klaim.nama == NamaJenisKlaimChoices.CBG_SUSULAN:
            data_klaim = DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim=self.nomor_register_klaim,
                                                     status=StatusDataKlaimChoices.PROSES)
            sisa_klaim = data_klaim.count()
        elif self.jenis_klaim.nama == NamaJenisKlaimChoices.OBAT_REGULER or self.jenis_klaim.nama == NamaJenisKlaimChoices.OBAT_SUSULAN:
            data_klaim = DataKlaimObat.objects.filter(register_klaim__nomor_register_klaim=self.nomor_register_klaim,
                                                      status=StatusDataKlaimChoices.PROSES)
            sisa_klaim = data_klaim.count()
        return sisa_klaim


    @classmethod
    def generate_kode_register(cls, faskes):
        kantor_cabang = faskes.kantor_cabang
        queryset = cls.objects.filter(faskes__kantor_cabang=kantor_cabang)
        if queryset.count() != 0:
            last_nomor = cls.objects.filter(faskes__kantor_cabang=kantor_cabang).last().nomor_register_klaim
        else:
            current_time = datetime.now()
            new_last_nomor = f'{kantor_cabang.kode_cabang}{str(current_time.year)[2:]}{str(current_time.month).zfill(2)}0001'
            return new_last_nomor

        year = int(last_nomor[4:6])
        month = int(last_nomor[6:8])
        increment = last_nomor[8:]

        current_year = datetime.now().year
        current_year = str(current_year)[2:]
        current_month = datetime.now().month
        if int(current_month) != int(month) or int(current_year) != int(year):
            increment = '1'.zfill(4)
        else:
            increment = int(increment)
            increment += 1
            increment = str(increment).zfill(4)

        new_last_nomor = f'{kantor_cabang.kode_cabang}{current_year}{str(current_month).zfill(2)}{increment}'

        if cls.objects.filter(nomor_register_klaim=new_last_nomor).exists():
            return cls.generate_kode_register(faskes=faskes)
        return new_last_nomor


class KeteranganPendingDispute(models.Model):
    ket_pending_dispute = models.CharField(max_length=1000)
    verifikator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ket_pending_dispute


class JawabanPendingDispute(models.Model):
    ket_jawaban_pending = models.CharField(max_length=1000)
    user_faskes = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ket_jawaban_pending


class DataKlaimCBG(models.Model):
    register_klaim = models.ForeignKey(RegisterKlaim, on_delete=models.CASCADE)
    faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE)
    verifikator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    bupel = models.DateField(blank=True, null=True)
    tgl_SLA = models.DateField(blank=True, null=True)
    ALGORITMA = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=200,
                              default=StatusDataKlaimChoices.BELUM_VER, choices=StatusDataKlaimChoices.choices)
    NOSEP = models.CharField(max_length=200, blank=True, null=True, unique=True)
    TGLSEP = models.DateField(blank=True, null=True)
    TGLPULANG = models.DateField(blank=True, null=True)
    JNSPEL = models.CharField(max_length=200, blank=True, null=True, choices=JenisPelayananChoices.choices)
    NOKARTU = models.CharField(max_length=200, blank=True, null=True)
    NMPESERTA = models.CharField(max_length=200, blank=True, null=True)
    POLI = models.CharField(max_length=200, blank=True, null=True)
    KDINACBG = models.CharField(max_length=200, blank=True, null=True)
    BYPENGAJUAN = models.PositiveBigIntegerField(default=0)
    ket_pending_dispute = models.ManyToManyField(KeteranganPendingDispute)
    ket_jawaban_pending = models.ManyToManyField(JawabanPendingDispute)
    # ket_pending_dispute = models.CharField(max_length=500, blank=True, null=True)
    # ket_jawaban_pending = models.CharField(max_length=500, blank=True, null=True)

    prosesklaim = models.BooleanField(default=False)
    prosespending = models.BooleanField(default=False)
    prosesdispute = models.BooleanField(default=False)
    prosestidaklayak = models.BooleanField(default=False)

    file_konfirmasi = models.FileField(upload_to='documents/', blank=True, null=True)
    jenis_pending = models.CharField(max_length=200, choices=JenisPendingChoices.choices, blank=True, null=True)
    jenis_dispute = models.CharField(max_length=200, choices=JenisDisputeChoices.choices, blank=True, null=True)
    klasifikasi_dispute = models.CharField(max_length=200, blank=True, null=True)
    keterangan_dispute = models.CharField(max_length=500, blank=True, null=True)
    proses_klasifikasi_dispute = models.BooleanField(default=False)
    is_hitung = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tgl_SLA is None:
            sla = SLA.objects.filter(jenis_klaim=self.register_klaim.jenis_klaim,
                                     kantor_cabang=self.faskes.kantor_cabang).first()
            if sla:
                if self.register_klaim.tgl_ba_lengkap:
                    self.tgl_SLA = self.register_klaim.tgl_ba_lengkap + timedelta(days=sla.plus_hari_sla)
                elif self.register_klaim.tgl_terima:
                    self.tgl_SLA = self.register_klaim.tgl_terima + timedelta(days=15)
            else:
                if self.register_klaim.tgl_ba_lengkap:
                    self.tgl_SLA = self.register_klaim.tgl_ba_lengkap + timedelta(days=6)
                elif self.register_klaim.tgl_terima:
                    self.tgl_SLA = self.register_klaim.tgl_terima + timedelta(days=15)
        self.bupel = self.TGLPULANG.replace(day=1)
        super(DataKlaimCBG, self).save(*args, **kwargs)


class DataKlaimObat(models.Model):
    register_klaim = models.ForeignKey(RegisterKlaim, on_delete=models.CASCADE)
    faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE)
    verifikator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    KdJenis = models.CharField(max_length=1, blank=True, null=True)
    NoSEPApotek = models.CharField(max_length=19, blank=True, null=True, unique=True)
    NoSEPAsalResep = models.CharField(max_length=19, blank=True, null=True)
    NoKartu = models.CharField(max_length=15, blank=True, null=True)
    NamaPeserta = models.CharField(max_length=200, blank=True, null=True)
    NoResep = models.CharField(max_length=15, blank=True, null=True)
    TglResep = models.DateField(blank=True, null=True)
    ByTagApt = models.IntegerField(default=0)
    ByVerApt = models.IntegerField(default=0)
    rufil = models.CharField(max_length=200, blank=True)

    status = models.CharField(max_length=20, default=StatusDataKlaimChoices.BELUM_VER, choices=StatusDataKlaimChoices.choices)
    bupel = models.DateField(blank=True, null=True)
    tgl_SLA = models.DateField(blank=True, null=True)

    ket_pending_dispute = models.ManyToManyField(KeteranganPendingDispute)
    ket_jawaban_pending = models.ManyToManyField(JawabanPendingDispute)

    prosesklaim = models.BooleanField(default=False)
    prosespending = models.BooleanField(default=False)
    prosesdispute = models.BooleanField(default=False)
    prosestidaklayak = models.BooleanField(default=False)

    file_konfirmasi = models.FileField(upload_to='documents/', blank=True, null=True)
    jenis_pending = models.CharField(max_length=200, choices=JenisPendingChoices.choices, blank=True, null=True)
    jenis_dispute = models.CharField(max_length=200, choices=JenisDisputeChoices.choices, blank=True, null=True)
    klasifikasi_dispute = models.CharField(max_length=200, blank=True, null=True)
    keterangan_dispute = models.CharField(max_length=500, blank=True, null=True)
    proses_klasifikasi_dispute = models.BooleanField(default=False)
    is_hitung = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tgl_SLA is None:
            sla = SLA.objects.filter(jenis_klaim=self.register_klaim.jenis_klaim,
                                     kantor_cabang=self.faskes.kantor_cabang).first()
            if sla:
                if self.register_klaim.tgl_ba_lengkap:
                    self.tgl_SLA = self.register_klaim.tgl_ba_lengkap + timedelta(days=sla.plus_hari_sla)
                elif self.register_klaim.tgl_terima:
                    self.tgl_SLA = self.register_klaim.tgl_terima + timedelta(days=15)
            else:
                if self.register_klaim.tgl_ba_lengkap:
                    self.tgl_SLA = self.register_klaim.tgl_ba_lengkap + timedelta(days=6)
                elif self.register_klaim.tgl_terima:
                    self.tgl_SLA = self.register_klaim.tgl_terima + timedelta(days=15)
        self.bupel = self.TglResep.replace(day=1)
        super(DataKlaimObat, self).save(*args, **kwargs)
