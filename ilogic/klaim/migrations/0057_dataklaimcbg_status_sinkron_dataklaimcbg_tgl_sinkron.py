# Generated by Django 4.2.5 on 2024-08-13 01:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("klaim", "0056_registerklaim_keterangan_potongklaim"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataklaimcbg",
            name="status_sinkron",
            field=models.CharField(
                choices=[("Tidak Sinkron", "Tidak Sinkron"), ("Sinkron", "Sinkron")],
                default="Belum Disinkron",
                max_length=200,
            ),
        ),
        migrations.AddField(
            model_name="dataklaimcbg",
            name="tgl_sinkron",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]