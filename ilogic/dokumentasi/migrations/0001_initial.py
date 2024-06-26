# Generated by Django 4.2.5 on 2023-11-23 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ICD10",
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
                ("kode", models.CharField(max_length=250)),
                ("nama", models.CharField(max_length=250)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProgressVersion",
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
                ("version", models.IntegerField(unique=True)),
                ("is_aju", models.BooleanField(default=False)),
                ("dt_is_aju", models.DateTimeField(blank=True, null=True)),
                ("is_approved_asdep", models.BooleanField(default=False)),
                ("dt_is_approved_asdep", models.DateTimeField(blank=True, null=True)),
                ("is_approved_depdirbid", models.BooleanField(default=False)),
                (
                    "dt_is_approved_depdirbid",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("open_edit", models.BooleanField(default=False)),
                ("dt_open_edit", models.DateTimeField(blank=True, null=True)),
                ("is_rejected", models.BooleanField(default=False)),
                ("dt_is_rejected", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PolaRules",
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
                ("nama_rules", models.CharField(max_length=250)),
                (
                    "diagnosis_utama",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "diagnosis_sekunder",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("prosedur", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "jenis_pelayanan",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("cmg", models.CharField(blank=True, max_length=250, null=True)),
                ("los", models.IntegerField(blank=True, null=True)),
                ("cbg", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "severity_level",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "jenis_kelamin",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("usia", models.IntegerField(blank=True, null=True)),
                ("pesan", models.TextField()),
                (
                    "models_polarules",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "progress_version",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dokumentasi.progressversion",
                    ),
                ),
            ],
        ),
    ]
