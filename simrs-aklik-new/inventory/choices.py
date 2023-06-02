from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusPembayaranChoices(models.TextChoices):
    BELUM_BAYAR = 'Belum Bayar', _('Belum Bayar')
    SUDAH_BAYAR = 'Sudah Bayar', _('Sudah Bayar')


class AsuransiChoices(models.TextChoices):
    UMUM = 'UMUM', _('UMUM')
    BPJS = 'BPJS', _('BPJS')