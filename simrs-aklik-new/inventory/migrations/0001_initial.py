# Generated by Django 3.2.12 on 2023-05-28 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pasien', '0006_remove_pendaftaran_kode_invoice'),
        ('antrian', '0005_alter_antrian_task_id'),
        ('kasir', '0003_summaryinvoice_totals'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlatKesehatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('harga', models.FloatField(default=0)),
                ('stok', models.IntegerField(default=0)),
                ('deskripsi', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlatKesehatanPasien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_pembayaran', models.CharField(choices=[('Belum Bayar', 'Belum Bayar'), ('Sudah Bayar', 'Sudah Bayar')], default='Belum Bayar', max_length=50)),
                ('harga', models.FloatField(default=0)),
                ('kuantitas', models.IntegerField(default=1)),
                ('total_harga', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('alat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.alatkesehatan')),
                ('antrian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antrian.antrian')),
                ('resume_medis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pasien.resumemedis')),
                ('summary_invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kasir.summaryinvoice')),
            ],
        ),
    ]
