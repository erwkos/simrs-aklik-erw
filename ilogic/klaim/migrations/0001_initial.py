# Generated by Django 4.2.2 on 2023-06-27 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('faskes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JenisKlaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=250, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegisterKlaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor_register_klaim', models.CharField(max_length=250, unique=True)),
                ('status', models.CharField(choices=[('Pengajuan', 'Pengajuan'), ('Terima', 'Terima'), ('Verifikasi', 'Verifikasi'), ('Selesai', 'Selesai'), ('Dikembalikan', 'Dikembalikan'), ('Proses FPK', 'Proses FPK'), ('Proses BOA', 'Proses BOA'), ('Pembayaran', 'Pembayaran')], default='Pengajuan', max_length=50)),
                ('kasus_rawat_jalan_aju', models.IntegerField(default=0)),
                ('biaya_rawat_jalan_aju', models.BigIntegerField(default=0)),
                ('kasus_rawat_inap_aju', models.IntegerField(default=0)),
                ('biaya_rawat_inap_aju', models.BigIntegerField(default=0)),
                ('bulan_pelayanan', models.DateField()),
                ('no_ba_terima', models.CharField(blank=True, max_length=25, null=True)),
                ('no_ba_lengkap', models.CharField(blank=True, max_length=25, null=True)),
                ('no_ba_hasil_verifikasi', models.CharField(blank=True, max_length=25, null=True)),
                ('tgl_terima', models.DateField(blank=True, null=True)),
                ('tgl_ba_lengkap', models.DateField(blank=True, null=True)),
                ('tgl_ba_verif', models.DateField(blank=True, null=True)),
                ('keterangan', models.CharField(blank=True, max_length=50, null=True)),
                ('absensi_klaim', models.CharField(blank=True, max_length=200, null=True)),
                ('tgl_aju', models.DateField(blank=True, null=True)),
                ('nomor_surat_pengajuan_rs', models.CharField(default='No Surat', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('faskes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faskes.faskes')),
                ('jenis_klaim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klaim.jenisklaim')),
            ],
        ),
    ]
