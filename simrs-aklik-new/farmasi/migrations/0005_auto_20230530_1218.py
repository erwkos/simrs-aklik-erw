# Generated by Django 3.2.12 on 2023-05-30 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmasi', '0004_obatpasien_status_layanan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='obat',
            name='harga',
        ),
        migrations.RemoveField(
            model_name='obat',
            name='stok',
        ),
        migrations.AddField(
            model_name='obat',
            name='date_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='disc_supplier',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='formularium',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='generik_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='group_obat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_dasar',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_eceran',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_jual_1',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_jual_2',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_jual_3',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_jual_4',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_jual_5',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_jual_eceran',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='harga_pembelian',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='hna',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='hna_ppn',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='inisial_kode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='isi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='jumlah_hari_utang',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='keterangan',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='kode_lokasi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='kode_pabrik',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='kode_satuan_besar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='kode_satuan_eceran',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='kode_satuan_kecil',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='main_gudang',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='obat',
            name='main_margin',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='margin_1',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='margin_2',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='margin_3',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='margin_4',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='margin_5',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='max_stok',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='min_stok',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='obat',
            name='stock_dis',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='obat',
            name='stok_reg',
            field=models.IntegerField(default=0),
        ),
    ]
