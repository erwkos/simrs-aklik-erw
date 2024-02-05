from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusRegisterChoices(models.TextChoices):
    PENGAJUAN = 'Pengajuan', _('Pengajuan')
    TERIMA = 'Terima', _('Terima')
    VERIFIKASI = 'Verifikasi', _('Verifikasi')
    SELESAI = 'Selesai', _('Selesai')
    DIKEMBALIKAN = 'Dikembalikan', _('Dikembalikan')
    # PROSES_FPK = 'Proses FPK', _('Proses FPK')  # FPHV (formulir persetujuan hasil verifikasi)
    # PROSES_BOA = 'Proses BOA', _('Proses BOA')
    # PEMBAYARAN = 'Pembayaran', _('Pembayaran')


class JenisDisputeChoices(models.TextChoices):
    MEDIS = 'Medis', _('Medis')
    KODING = 'Koding', _('Koding')
    OBAT = 'Obat', _('Obat')
    COB = 'COB', _('COB')


class JenisPendingChoices(models.TextChoices):
    ADMINISTRASI = 'Kelengkapan Administrasi', _('Kelengkapan Administrasi')
    KODING = 'Kaidah Koding', _('Kaidah Koding')
    STANDAR_PELAYANAN = 'Standar Pelayanan', _('Standar Pelayanan')


class JenisPelayananChoices(models.TextChoices):
    RAWAT_INAP = 'Rawat Inap', _('Rawat Inap')
    RAWAT_JALAN = 'Rawat Jalan', _('Rawat Jalan')


class StatusDataKlaimChoices(models.TextChoices):
    PEMBAHASAN = 'Pembahasan', _('Pembahasan')
    TIDAK_LAYAK = 'Tidak Layak', _('Tidak Layak')
    LAYAK = 'Layak', _('Layak')
    PENDING = 'Pending', _('Pending')
    DISPUTE = 'Dispute', _('Dispute')
    KLAIM = 'Klaim', _('Klaim')
    BELUM_VER = 'Belum Ver', _('Belum Ver')
    PROSES = 'Proses', _('Proses')


# penambahan suatu jenis klaim dari sini
class NamaJenisKlaimChoices(models.TextChoices):
    CBG_REGULER = 'CBG-Reguler', _('CBG-Reguler')
    CBG_SUSULAN = 'CBG-Susulan-Pending-Dispute', _('CBG-Susulan-Pending-Dispute')
    OBAT_REGULER = 'Obat-Reguler', _('Obat-Reguler')
    OBAT_SUSULAN = 'Obat-Susulan-Pending-Dispute', _('Obat-Susulan-Pending-Dispute')
    OPTIK = 'Optik', _('Optik')
    CAPD = 'CAPD', _('CAPD')
    AMBULANCE_FKRTL = 'Ambulance-FKRTL', _('Ambulance-FKRTL')
    ALKES = 'Alkes', _('Alkes')
