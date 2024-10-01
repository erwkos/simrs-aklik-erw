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
    SudahKoreksi = 'Sudah Koreksi', _('Sudah Koreksi')


class InisiasiChoices(models.TextChoices):
    VPK = 'Hasil Verifikasi Pascaklaim', _('Verifikasi Pascaklaim')
    UR = 'Hasil UR dan Deteksi Potensi Kecurangan', _('UR dan Deteksi Potensi Kecurangan')
    WBS = 'Whistle Blowing System', _('Whistle Blowing System')
    AUDITOR = 'Hasil Audit oleh Auditor', _('Hasil Audit oleh Auditor')
    AM = 'Hasil Audit Medis', _('Hasil Audit Medis')


class StatusKoreksiBoaChoices(models.TextChoices):
    BELUM = 'Belum Koreksi BOA', _('Belum Koreksi BOA')
    SELESAI = 'Selesai Koreksi BOA', _('Selesai Koreksi BOA')
    GAGAL = 'Gagal Koreksi BOA', _('Gagal Koreksi BOA')
    PROSES = 'Sudah Proses Koreksi di BOA', _('Sudah Proses Koreksi di BOA')


class JenisFraudChoices(models.TextChoices):
    ManipulasiDiagnosis = 'Memanipulasi diagnosis dan/atau tindakan', _('Memanipulasi diagnosis dan/atau tindakan')
    Cloning = 'Penjiplakan klaim dari pasien lain (Cloning)', _('Penjiplakan klaim dari pasien lain (Cloning)')
    PhantomBilling = 'Klaim palsu (Phantom Billing)', _('Klaim palsu (Phantom Billing)')
    InflatedBills = 'Penggelembungan tagihan obat dan/atau alat kesehatan (Inflated Bills)', _('Penggelembungan tagihan obat dan/atau alat kesehatan (Inflated Bills)')
    PemecahanEpisodeSesuaiIndikasiMedis = 'Pemecahan episode pelayanan sesuai dengan indikasi medis tetapi tidak sesuai dengan ketentuan peraturan perundang-undangan', _('Pemecahan episode pelayanan sesuai dengan indikasi medis tetapi tidak sesuai dengan ketentuan peraturan perundang-undangan')
    PemecahanEpisodeTidakSesuaiIndikasiMedis = 'Pemecahan episode pelayanan yang tidak sesuai dengan indikasi medis (Services Unbundling or Fragmentation)', _('Pemecahan episode pelayanan yang tidak sesuai dengan indikasi medis (Services Unbundling or Fragmentation)')
    SelfReferals = 'Rujukan semu (Self-Referals)', _('Rujukan semu (Self-Referals)')
    ProlongedLOS = 'Memperpanjang lama perawatan (Prolonged Length of Stay)', _('Memperpanjang lama perawatan (Prolonged Length of Stay)')
    ManipulationRoomCharge = 'Memanipulasi kelas perawatan (Manipulation of Room Charge)', _('Memanipulasi kelas perawatan (Manipulation of Room Charge)')
    PenagihanTindakanTidakDilakukan = 'Menagihkan tindakan yang tidak dilakukan', _('Menagihkan tindakan yang tidak dilakukan')
    TindakanTidakIndikasiMedis = 'Melakukan tindakan pengobatan yang tidak sesuai dengan indikasi medis', _('Melakukan tindakan pengobatan yang tidak sesuai dengan indikasi medis')
    Readmisi = 'Admisi yang berulang (Readmisi)', _('Admisi yang berulang (Readmisi)')
    IurBiaya = 'Menarik biaya dari Peserta tidak sesuai dengan ketentuan peraturan perundang-undangan', _('Menarik biaya dari Peserta tidak sesuai dengan ketentuan peraturan perundang-undangan')
    TidakFraud = 'Temuan Administrasi yang tidak sesuai atau alasan lain yang bukan potensi fraud', _('Temuan Administrasi yang tidak sesuai atau alasan lain yang bukan potensi fraud')

