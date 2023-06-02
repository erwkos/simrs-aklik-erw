from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusPembayaranChoices(models.TextChoices):
    TELAH_DIBAYAR = 'TELAH_DIBAYAR', _('Telah bayar')
    BELUM_BAYAR = 'BELUM_BAYAR', _('Belum bayar')



class KondisiUmumChoices(models.TextChoices):
    BAIK = 'BAIK', _('Baik')
    BURUK = 'BURUK', _('Buruk')
    SEDANG = 'SEDANG', _('Sedang')


class KesadaranChoices(models.TextChoices):
    COMPOS_MENTIS = 'COMPOS_MENTIS', _('Compos Mentis')
    APATIS = 'APATIS', _('Apatis')
    SOMNOLEN = 'SOMNOLEN', _('Somnolen')
    SOPOR = 'SOPOR', _('Sopor')
    COMA = 'COMA', _('Coma')


class IsiChoices(models.TextChoices):
    CUKUP = 'CUKUP', _('Cukup')
    KURANG = 'KURANG', _('Kurang')
    LEMAH = 'LEMAH', _('Lemah')


class RujukanChoices(models.TextChoices):
    FASKES_1 = 'FASKES_1', _('Faskes 1')
    POLISI = 'POLISI', _('Polisi')
    SENDIRI = 'SENDIRI', _('Sendiri')
    RUMAH_SAKIT = 'RUMAH_SAKIT', _('Rumah sakit')
    PUSKESMAS = 'PUSKESMAS', _('Puskesmas')
    FASILITAS_KESEHATAN_LAIN = 'FASILITAS_KESEHATAN_LAIN', _('Fasilitas kesehatan lain')
    DOKTER_KELUARGA = 'DOKTER_KELUARGA', _('Dokter keluarga')
    LAINNYA = 'LAINNYA', _('Lainnya')
    DATANG_SENDIRI = 'DATANG_SENDIRI', _('Datang sendiri')


class KeadaanKeluarChoices(models.TextChoices):
    DIRUJUK_RS_LAIN = 'DIRUJUK_RS_LAIN', _('Dirujuk rs lain')
    SEMBUH = 'SEMBUH', _('Sembuh')
    MENINGGAL_KURANG_8_JAM = 'MENINGGAL_KURANG_8_JAM', _('Meninggal < 8 jam')
    MENINGGAL_LEBIH_8_JAM = 'MENINGGAL_LEBIH_8_JAM', _('Meninggal > 8 jam')
    BELUM_SEMBUH = 'BELUM_SEMBUH', _('Belum sembuh')
    MENINGGAL_KURANG_48_JAM = 'MENINGGAL_KURANG_48_JAM', _('Meninggal < 48 jam')
    MENINGGAL_LEBIH_48_JAM = 'MENINGGAL_LEBIH_48_JAM', _('Meninggal > 48 jam')
    DIIJINKAN_PULANG = 'DIIJINKAN_PUULANG', _('Diijinkan pulang')


class CaraKeluarChoices(models.TextChoices):
    DIRUJUK = 'DIRUJUK', _('Dirujuk')
    ATAS_PERSETUJUAN_DOKTER = 'ATAS_PERSETUJUAN_DOKTER', _('Atas persutujuan dokter')
    LAIN_LAIN = 'LAIN_LAIN', _('Lain-lain')
    ATAS_PERMINTAAN_SENDIRI = 'ATAS_PERMINTAAN_SENDIRI', _('Atas permintaan sendiri')
    MELARIKAN_DIRI = 'MELARIKAN_DIRI', _('Melarikan diri')
    MENINGGAL = 'MENINGGAL', _('Meninggal')


class PemeriksaanLanjutan(models.TextChoices):
    KONTROL = 'KONTROL', _('Kontrol')
    BANGSAL = 'BANGSAL', _('Bangsal')
    POLIKLINIK_RS = 'POLIKLINIK_RS', _('Poliklinik rs')
    RS_LAIN = 'RS_LAIN', _('RS lain')
    PUSKESMAS = 'PUSKESMAS', _('Puskesmas')
    LAINNYA = 'LAINNYA', _('Lainnya')
    TIDAK_ADA = 'TIDAK_ADA', _('Tidak ada')


class StatusGeneralisChoices(models.TextChoices):
    NORMAL = 'NORMAL', _('Normal')
    ABNORMAL = 'ABNORMAL', _('Abnormal')


class StatusPembayaranChoices(models.TextChoices):
    BELUM_BAYAR = 'Belum Bayar', _('Belum Bayar')
    SUDAH_BAYAR = 'Sudah Bayar', _('Sudah Bayar')
