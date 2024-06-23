# Generated by Django 4.2.5 on 2023-12-05 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("faskes", "0005_alter_faskes_user_alter_kantorcabang_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("klaim", "0050_alter_sla_kantor_cabang"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataKlaimObat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("KdJenis", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "NoSEPApotek",
                    models.CharField(
                        blank=True, max_length=200, null=True, unique=True
                    ),
                ),
                (
                    "NoSEPAsalResep",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("NoKartu", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "NamaPeserta",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("NoResep", models.CharField(blank=True, max_length=200, null=True)),
                ("TglResep", models.DateField(blank=True, null=True)),
                ("ByTagApt", models.IntegerField(default=0)),
                ("ByVerApt", models.IntegerField(default=0)),
                ("rufil", models.CharField(blank=True, max_length=200)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pembahasan", "Pembahasan"),
                            ("Tidak Layak", "Tidak Layak"),
                            ("Layak", "Layak"),
                            ("Pending", "Pending"),
                            ("Dispute", "Dispute"),
                            ("Klaim", "Klaim"),
                            ("Belum Ver", "Belum Ver"),
                            ("Proses", "Proses"),
                        ],
                        default="Belum Ver",
                        max_length=200,
                    ),
                ),
                ("bupel", models.DateField(blank=True, null=True)),
                ("tgl_SLA", models.DateField(blank=True, null=True)),
                ("prosesklaim", models.BooleanField(default=False)),
                ("prosespending", models.BooleanField(default=False)),
                ("prosesdispute", models.BooleanField(default=False)),
                ("prosestidaklayak", models.BooleanField(default=False)),
                (
                    "file_konfirmasi",
                    models.FileField(blank=True, null=True, upload_to="documents/"),
                ),
                (
                    "jenis_pending",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Kelengkapan Administrasi", "Kelengkapan Administrasi"),
                            ("Kaidah Koding", "Kaidah Koding"),
                            ("Standar Pelayanan", "Standar Pelayanan"),
                        ],
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "jenis_dispute",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Medis", "Medis"),
                            ("Koding", "Koding"),
                            ("Obat", "Obat"),
                            ("COB", "COB"),
                        ],
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "klasifikasi_dispute",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "keterangan_dispute",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("proses_klasifikasi_dispute", models.BooleanField(default=False)),
                ("is_hitung", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "faskes",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="faskes.faskes"
                    ),
                ),
                (
                    "ket_jawaban_pending",
                    models.ManyToManyField(to="klaim.jawabanpendingdispute"),
                ),
                (
                    "ket_pending_dispute",
                    models.ManyToManyField(to="klaim.keteranganpendingdispute"),
                ),
                (
                    "register_klaim",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="klaim.registerklaim",
                    ),
                ),
                (
                    "verifikator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]