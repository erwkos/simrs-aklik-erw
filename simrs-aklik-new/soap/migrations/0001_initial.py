# Generated by Django 3.2.12 on 2023-05-26 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('antrian', '0001_initial'),
        ('pasien', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentICD10',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(blank=True, max_length=100, null=True)),
                ('kode', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subjective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keluhan_utama', models.TextField(blank=True, null=True)),
                ('kondisi_umum', models.CharField(blank=True, choices=[('Baik', 'Baik'), ('Buruk', 'Buruk'), ('Sedang', 'Sedang')], max_length=100, null=True)),
                ('riwayat_penyakit_dahulu', models.TextField(blank=True, null=True)),
                ('riwayat_penyakit_sekarang', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('antrian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antrian.antrian')),
                ('resume_medis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pasien.resumemedis')),
            ],
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rencana_tindakan', models.TextField(blank=True, null=True)),
                ('terapi_obat_obatan', models.TextField(blank=True, null=True)),
                ('rencana_konsultasi', models.TextField(blank=True, null=True)),
                ('rencana_rawat', models.CharField(blank=True, max_length=10, null=True)),
                ('rencana_perawatan_pasca_rawat', models.CharField(blank=True, max_length=150, null=True)),
                ('antrian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antrian.antrian')),
                ('resume_medis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pasien.resumemedis')),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kesadaran', models.CharField(blank=True, choices=[('Compos Mentis', 'Compos Mentis'), ('Apatis', 'Apatis'), ('Somnolen', 'Somnolen'), ('Sopor', 'Sopor'), ('Coma', 'Coma')], max_length=100, null=True)),
                ('tensi_sistol', models.CharField(blank=True, max_length=50, null=True)),
                ('tensi_diastol', models.CharField(blank=True, max_length=50, null=True)),
                ('nadi', models.CharField(blank=True, max_length=50, null=True)),
                ('rr', models.CharField(blank=True, max_length=50, null=True)),
                ('suhu', models.CharField(blank=True, max_length=50, null=True)),
                ('down_score', models.CharField(blank=True, max_length=50, null=True)),
                ('trauma_score', models.CharField(blank=True, max_length=50, null=True)),
                ('meows_score', models.CharField(blank=True, max_length=50, null=True)),
                ('berat_badan', models.CharField(blank=True, max_length=50, null=True)),
                ('tinggi_badan', models.CharField(blank=True, max_length=50, null=True)),
                ('gcs_e', models.CharField(blank=True, max_length=50, null=True)),
                ('gcs_m', models.CharField(blank=True, max_length=50, null=True)),
                ('gcs_v', models.CharField(blank=True, max_length=50, null=True)),
                ('kepala', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('mata', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('telinga', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('hidung', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('gigi', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('mulut', models.CharField(choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100)),
                ('leher', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('wajah', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('thorax', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('paru_paru', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('jantung', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('abdomen', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('hati', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('limpa', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('generalia', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Abnornal', 'Abnormal')], default='Normal', max_length=100, null=True)),
                ('ekstrimitas', models.TextField(blank=True, null=True)),
                ('status_lokalis', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('antrian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antrian.antrian')),
                ('resume_medis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pasien.resumemedis')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentICD9',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(blank=True, max_length=100, null=True)),
                ('kode', models.CharField(blank=True, max_length=100, null=True)),
                ('antrian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antrian.antrian')),
            ],
        ),
    ]
