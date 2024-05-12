from django.db import models
from django.utils.translation import gettext_lazy as _


class JenisAuditChoices(models.TextChoices):
    AAK = 'AAK-FKRTL', _('AAK-FKRTL')
    VPK = 'VPK-FKRTL', _('VPK-FKRTL')


class KelasFaskesChoices(models.TextChoices):
    A = 'A', _('A')
    B = 'B', _('B')
    C = 'C', _('C')
    D = 'D', _('D')


class StatusChoices(models.TextChoices):
    Register = 'Register', _('Register')
    Verifikasi = 'Proses Review', _('Proses Review')
    Finalisasi = 'Selesai', _('Selesai')


class StatusReviewChoices(models.TextChoices):
    Belum = 'Belum Review', _('Belum Review')
    Sesuai = 'Sesuai', _('Sesuai')
    TidakSesuai = 'Tidak Sesuai', _('Tidak Sesuai')


class InisiasiChoices(models.TextChoices):
    VPK = 'Hasil Verifikasi Pascaklaim', _('Verifikasi Pascaklaim')
    UR = 'Hasil UR dan Deteksi Potensi Kecurangan', _('UR dan Deteksi Potensi Kecurangan')
    WBS = 'Whistle Blowing System', _('Whistle Blowing System')
    AUDITOR = 'Hasil Audit oleh Auditor', _('Hasil Audit oleh Auditor')
    AM = 'Hasil Audit Medis', _('Hasil Audit Medis')
