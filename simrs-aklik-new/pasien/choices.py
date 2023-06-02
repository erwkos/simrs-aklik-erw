from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusPasienChoices(models.TextChoices):
    BARU = 'BARU', _('Baru')
    LAMA = 'LAMA', _('Lama')


class JenisKelamin(models.TextChoices):
    WANITA = 'WANITA', _('Wanita')
    PRIA = 'PRIA', _('Pria')


class TipeLayanan(models.TextChoices):
    IGD = 'IGD', _('IGD')
    RAWAT_JALAN = 'RAWAT_JALAN', _('Rawat Jalan')


class StatusLayananChoices(models.TextChoices):
    BERLANGSUNG = 'Berlangsung', _('Berlangsung')
    SELESAI = 'Selesai', _('Selesai')


class AgamaChoices(models.TextChoices):
    ISLAM = 'Islam', _('Islam')
    KRISTEN_PROTESTAN = 'Kristen Protestan', _('kristen Protestan')
    KRISTEN_KATOLIK = 'Kristen Katolik', _('Kristen Katolik')
    HINDU = 'Hindu', _('Hindu')
    BUDHA = 'Buddha', _('Buddha')
    KONGHUCU = 'Konghucu', _('Konghucu')


class StatusPembayaranChoices(models.TextChoices):
    BELUM_BAYAR = 'Belum Bayar', _('Belum Bayar')
    SUDAH_BAYAR = 'Sudah Bayar', _('Sudah Bayar')
    BATAL = 'Batal', _('Batal')


class AsuransiChoices(models.TextChoices):
    UMUM = 'UMUM', _('UMUM')
    BPJS = 'BPJS', _('BPJS')


class RujukanChoices(models.TextChoices):
    FASKES_1 = 'Fasekes 1', _('Fasekes 1')
    POLISI = 'Polisi', _('Polisi')
    SENDIRI = 'Sendiri', _('Sendiri')
    RUMAH_SAKIT = 'Rumah Sakit', _('Rumah Sakit')
    PUSKESMAS = 'Puskesmas', _('Puskesmas')
    FASILITAS_KESEHATAN_LAIN = 'Fasilitas Kesehatan Lain', _('Fasilitas Kesehatan Lain')
    DOKTER_KELUARGA = 'Dokter Keluarga', _('Dokter Keluarga')


class KeadanKeluarChoices(models.TextChoices):
    DIRIJUK_KE_RS_LAIN = 'Dirujuk Ke RS Lain', _('Dirujuk Ke RS Lain')
    SEMBUH = 'Sembuh', _('Sembuh')
    BELUM_SEMBUH = 'Belum Sembuh', _('Belum Sembuh')
    MENINGGAL_KURANG_8_JAM = 'Meninggal Kurang 8 Jam', _('Meninggal Kurang 8 Jam')
    MENINGGAL_LEBIH_8_JAM = 'Meninggal Lebih 8 Jam', _('Meninggal Kurang 8 Jam')
    MENINGGAL_KURANG_48_JAM = 'Meninggal Kurang 48 Jam', _('Meninggal Kurang 48 Jam')
    MENINGGAL_LEBIH_48_JAM = 'Meninggal Lebih 48 Jam', _( 'Meninggal Lebih 48 Jam')
    DIIJINKAN_PULANG = 'Diijinkan Pulang', _('Diijinkan Pulang')


class CaraKeluarChoices(models.TextChoices):
    DIRUJUK = 'Dirujuk', _('Dirujuk')
    ATAS_PERSETUJUAN_DOKTER = 'Atas Persetujuan Dokter', _('Atas Persetujuan Dokter')
    ATAS_PERMINTAAN_SENDIRI = 'Atas Permintaan Sendiri', _('Atas Permintaan Sendiri')
    MELARIKAN_DIRI = 'Melarikan Diri', _('Melarikan Diri')
    MENINGGAL = 'Meninggal', _('Meninggal')
    LAINNYA = 'Lainnya', _('Lainnya')


class PemeriksaanLanjutChoices(models.TextChoices):
    KONTROL = 'Kontrol', _('Kontrol')
    BANGSAL = 'Bangsal', _('Bangsal')
    POLIKLINIK_RS = 'Poliklinik RS', _('Poliklinik RS')
    RS_LAIN = 'RS Lain', _('RS Lain')
    PUSKESMAS = 'Puskesmas', _('Puskesmas')
    LAINNYA = 'Lainnya', _('Lainnya')

