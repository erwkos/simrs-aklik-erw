# Generated by Django 3.2.12 on 2023-05-26 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kasir', '0002_initial'),
        ('pasien', '0001_initial'),
        ('lab', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='layananlabpasien',
            name='dokter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_dokter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='layananlabpasien',
            name='layanan_lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.layananlab'),
        ),
        migrations.AddField(
            model_name='layananlabpasien',
            name='petugas_lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_petugas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='layananlabpasien',
            name='resume_medis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pasien.resumemedis'),
        ),
        migrations.AddField(
            model_name='layananlabpasien',
            name='summary_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kasir.summaryinvoice'),
        ),
        migrations.AddField(
            model_name='layananlab',
            name='kategori',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.kategorilayananlab'),
        ),
        migrations.AddField(
            model_name='hasilsublayananlab',
            name='layanan_lab_pasien',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.layananlabpasien'),
        ),
        migrations.AddField(
            model_name='hasilsublayananlab',
            name='sub_layanan_lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.sublayananlab'),
        ),
    ]
