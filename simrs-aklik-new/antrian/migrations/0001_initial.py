# Generated by Django 3.2.12 on 2023-05-26 17:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Antrian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_antrian', models.IntegerField()),
                ('no_rekam_medis', models.CharField(max_length=100)),
                ('tanggal_periksa', models.DateField()),
                ('waktu_start_mengantri', models.DateTimeField(auto_now_add=True)),
                ('waktu_end_mengantri', models.DateTimeField(blank=True, null=True)),
                ('waktu_start_layanan', models.DateTimeField(blank=True, null=True)),
                ('waktu_end_layanan', models.DateTimeField(blank=True, null=True)),
                ('task_id', models.IntegerField(default=1)),
                ('antrian_tanggal', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('nama', models.CharField(max_length=100)),
                ('loket', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
