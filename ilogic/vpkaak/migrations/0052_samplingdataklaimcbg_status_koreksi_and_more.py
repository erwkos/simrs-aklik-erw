# Generated by Django 4.2.5 on 2024-09-01 04:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "vpkaak",
            "0051_rename_is_status_koreksi_boa_samplingdataklaimcbg_status_koreksi_boa",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="status_koreksi",
            field=models.CharField(default="Belum Koreksi", max_length=255),
        ),
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="keterangan_koreksi_boa",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
