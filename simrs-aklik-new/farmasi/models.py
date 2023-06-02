from django.db import models

from user.models import User
from .choices import StatusPembayaranChoices, StatusLayananChoices, StatusObatChoices
from kasir.models import SummaryInvoice


class PetugasFarmasi(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Obat(models.Model):
    nama = models.CharField(max_length=150)
    harga = models.FloatField(default=0)
    stok = models.IntegerField(default=0)
    inisial_kode = models.CharField(max_length=100, blank=True, null=True)
    kode = models.CharField(max_length=100, blank=True, null=True)
    kode_satuan_besar = models.CharField(max_length=100, blank=True, null=True)
    kode_satuan_kecil = models.CharField(max_length=100, blank=True, null=True)
    kode_satuan_eceran = models.CharField(max_length=100, blank=True, null=True)

    harga_jual_1 = models.FloatField(default=0)
    harga_jual_2 = models.FloatField(default=0)
    harga_jual_3 = models.FloatField(default=0)
    harga_jual_4 = models.FloatField(default=0)
    harga_jual_5 = models.FloatField(default=0)
    harga_jual_eceran = models.FloatField(default=0)

    margin_1 = models.FloatField(default=0)
    margin_2 = models.FloatField(default=0)
    margin_3 = models.FloatField(default=0)
    margin_4 = models.FloatField(default=0)
    margin_5 = models.FloatField(default=0)

    harga_eceran = models.FloatField(default=0)

    isi = models.IntegerField(default=0)

    harga_dasar = models.FloatField(default=0)

    hna = models.FloatField(default=0)
    ppn = models.FloatField(default=0)
    harga_pembelian = models.FloatField(default=0)

    min_stok = models.IntegerField(default=0)
    max_stok = models.IntegerField(default=0)

    main_gudang = models.CharField(max_length=100, blank=True, null=True)

    disc_supplier = models.CharField(max_length=100, blank=True, null=True)

    # jenis_barang

    # id_supplier = models.IntegerField()

    # relasi_satuan

    group_obat = models.CharField(max_length=100, blank=True, null=True)

    formularium = models.CharField(max_length=100, blank=True, null=True)

    stock_dis = models.IntegerField(default=0)

    status = models.CharField(max_length=20, choices=StatusObatChoices.choices, default=StatusObatChoices.ACTIVE)

    # user_entry
    # data_entry
    # user_update
    date_update = models.DateTimeField(blank=True, null=True)

    kode_pabrik = models.CharField(max_length=100, blank=True, null=True)
    kode_lokasi = models.CharField(max_length=100, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)

    stok_reg = models.IntegerField(default=0)
    generik_status = models.CharField(max_length=100, blank=True, null=True)

    jumlah_hari_utang = models.IntegerField(default=0)

    # askes_status
    # main_disc
    main_margin = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class ObatPasien(models.Model):
    antrian = models.ForeignKey('antrian.Antrian', on_delete=models.SET_NULL, blank=True, null=True)
    resume_medis = models.ForeignKey('pasien.ResumeMedis', on_delete=models.SET_NULL, blank=True, null=True)
    dokter = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='farmasi_dokter')
    petugas_farmasi = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='farmasi_petugas')
    obat = models.ForeignKey(Obat, on_delete=models.SET_NULL, blank=True, null=True)
    harga = models.FloatField()
    kuantitas = models.IntegerField(default=0)
    total_harga = models.FloatField()
    status_pembayaran = models.CharField(max_length=30, choices=StatusPembayaranChoices.choices,
                                         default=StatusPembayaranChoices.BELUM_BAYAR)
    status_layanan = models.CharField(max_length=30,
                                      choices=StatusLayananChoices.choices,
                                      default=StatusLayananChoices.MENUNGGU)
    summary_invoice = models.ForeignKey(SummaryInvoice, on_delete=models.SET_NULL, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deskripsi = models.TextField(blank=True, null=True)



