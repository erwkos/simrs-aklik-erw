from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinLengthValidator

from faskes.models import Faskes
from vpkaak.choices import JenisAuditChoices, KelasFaskesChoices, StatusChoices, InisiasiChoices, StatusReviewChoices
from user.models import User


# Create your models here.
class RegisterPostKlaim(models.Model):
    nomor_register = models.CharField(max_length=255, blank=True, null=True)
    jenis_audit = models.CharField(max_length=10, choices=JenisAuditChoices.choices)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, blank=True, null=True)
    nomor_BA_VPK_AAK = models.CharField(max_length=255, null=True, blank=True)
    tanggal_BA_VPK_AAK = models.DateField(null=True, blank=True)
    is_final = models.BooleanField(default=False)
    tanggal_final = models.DateField(null=True, blank=True)
    biaya_efisiensi = models.IntegerField(null=True, blank=True)
    # AAK
    inisiasi = models.CharField(max_length=255, choices=InisiasiChoices.choices, null=True, blank=True)
    periode_awal = models.DateField(null=True, blank=True)
    periode_akhir = models.DateField(null=True, blank=True)
    surat_tugas = models.CharField(max_length=255, null=True, blank=True)
    # VPK
    bulan_beban = models.DateField(null=True, blank=True)
    # staff_upk = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="staff_upk")
    # verifikator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="verifikator")
    # faskes = models.ForeignKey(Faskes, on_delete=models.CASCADE, null=True, blank=True, related_name="faskes")
    # kelas = models.CharField(max_length=10, choices=KelasFaskesChoices.choices, blank=True, null=True)

    is_kp = models.BooleanField(default=False)
    # is_from_kp = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_register")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nomor_register


# @receiver(pre_save, sender=RegisterPostKlaim)
# def generate_nama_register(sender, instance, **kwargs):
#     if not instance.nomor_register_klaim:
#         if instance.jenis_audit == 'AAK-FKRTL':
#             jenis_audit_prefix = 'AAK-FKRTL'
#         elif instance.jenis_audit == 'VPK-FKRTL':
#             jenis_audit_prefix = 'VPK-FKRTL'
#         else:
#             jenis_audit_prefix = 'OTHER'
#         bulan_tahun = timezone.now().strftime("%m%y")
#         max_nomor_urut = RegisterPostKlaim.objects.filter(
#             nomor_register_klaim__startswith=f"001/{jenis_audit_prefix}/{instance.user.kantor_cabang.kode_cabang}/{bulan_tahun}"
#         ).aggregate(Max('nomor_register_klaim'))
#         if max_nomor_urut['nomor_register_klaim__max']:
#             nomor_urut = int(max_nomor_urut['nomor_register_klaim__max'].split('/')[0])
#             nomor_urut += 1
#         else:
#             nomor_urut = 1
#
#         instance.nomor_register_klaim = f"{nomor_urut:03d}/{jenis_audit_prefix}/{instance.user.kantor_cabang.kode_cabang}/{bulan_tahun}"


class SamplingDataKlaimCBG(models.Model):
    register = models.ForeignKey(RegisterPostKlaim, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=StatusReviewChoices.choices, default="Belum Review")

    # dataklaimcbg
    Nokapst = models.CharField(max_length=255)
    Tgldtgsjp = models.DateField()
    Tglplgsjp = models.DateField()
    Nosjp = models.CharField(max_length=255)
    Tglpelayanan = models.DateField()
    Kdkrlayan = models.CharField(max_length=255)
    Kdkclayan = models.CharField(max_length=255, validators=[MinLengthValidator(4)])
    Nmkclayan = models.CharField(max_length=255)
    Kddati2Layan = models.CharField(max_length=255)
    Nmdati2Layan = models.CharField(max_length=255)
    Kdppklayan = models.CharField(max_length=255)
    Nmppklayan = models.CharField(max_length=255)
    Nmtkp = models.CharField(max_length=255)
    Kdinacbgs = models.CharField(max_length=255)
    Nminacbgs = models.CharField(max_length=255)
    Kddiagprimer = models.CharField(max_length=255)
    Nmdiagprimer = models.CharField(max_length=255)
    Diagsekunder = models.CharField(max_length=5000, blank=True, null=True)
    Procedure = models.CharField(max_length=5000, blank=True, null=True)
    Klsrawat = models.CharField(max_length=255)
    Nmjnspulang = models.CharField(max_length=255)
    kddokter = models.CharField(max_length=255, blank=True, null=True)
    nmdokter = models.CharField(max_length=255, blank=True, null=True)
    Umur = models.IntegerField()
    Jkpst = models.CharField(max_length=10, blank=True, null=True)
    kdsa = models.CharField(max_length=255)
    kdsd = models.CharField(max_length=255)
    deskripsisd = models.CharField(max_length=255, default='-', blank=True, null=True)
    kdsi = models.CharField(max_length=255)
    deskripsisi = models.CharField(max_length=255, default='-', blank=True, null=True)
    kdsp = models.CharField(max_length=255)
    deskripsisp = models.CharField(max_length=255, default='-', blank=True, null=True)
    kdsr = models.CharField(max_length=255)
    deskripsisr = models.CharField(max_length=255)
    Tarifgroup = models.IntegerField()
    tarifsa = models.IntegerField()
    tarifsd = models.IntegerField()
    tarifsi = models.IntegerField()
    tarifsp = models.IntegerField()
    tarifsr = models.IntegerField()
    Biayaverifikasi = models.IntegerField()
    redflag = models.CharField(max_length=500, blank=True, null=True)
    deskripsi_redflag = models.CharField(max_length=1000, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    # databayi
    is_bayi = models.BooleanField(default=False)
    beratbayi = models.IntegerField(default=0)
    tanggallahirbayi = models.DateField(blank=True, null=True)

    # datars
    Kodersmenkes = models.CharField(max_length=15, blank=True, null=True)
    Kelasrsmenkes = models.CharField(max_length=10, blank=True, null=True)

    # hasil koreksi
    is_koreksi = models.BooleanField(default=False)
    Kddiagprimer_koreksi = models.CharField(max_length=5000, blank=True, null=True)
    Nmdiagprimer_koreksi = models.CharField(max_length=5000, blank=True, null=True)
    Diagsekunder_koreksi = models.CharField(max_length=5000, blank=True, null=True)
    Procedure_koreksi = models.CharField(max_length=5000, blank=True, null=True)
    kdsa_koreksi = models.CharField(max_length=255, blank=True, null=True)
    kdsd_koreksi = models.CharField(max_length=255, blank=True, null=True)
    kdsi_koreksi = models.CharField(max_length=255, blank=True, null=True)
    kdsp_koreksi = models.CharField(max_length=255, blank=True, null=True)
    kdsr_koreksi = models.CharField(max_length=255, blank=True, null=True)
    Nmtkp_koreksi = models.CharField(max_length=255, blank=True, null=True)
    Kdinacbgs_koreksi = models.CharField(max_length=255, blank=True, null=True)
    Nminacbgs_koreksi = models.CharField(max_length=255, blank=True, null=True)
    Klsrawat_koreksi = models.CharField(max_length=255, blank=True, null=True)
    biaya_koreksi = models.IntegerField(blank=True, null=True)

    # review
    tgl_review = models.DateTimeField(blank=True, null=True)
    verifikator_review = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    keterangan_review = models.CharField(max_length=1000, blank=True, null=True, validators=[MinLengthValidator(10)])

    # identity
    is_from_kp = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.Nosjp} - {self.register.nomor_register}'


class CookiesICD(models.Model):
    cookie_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cookie_value
