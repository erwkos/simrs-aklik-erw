# Generated by Django 4.2.5 on 2024-08-23 03:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpkaak", "0045_alter_samplingdataklaimcbg_kodersmenkes"),
    ]

    operations = [
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="is_status_koreksi_boa",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="jenis_fraud",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="tgl_koreksi_boa",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
