# Generated by Django 4.2.5 on 2024-04-28 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vpkaak", "0014_samplingdataklaimcbg_klsrawat_koreksi"),
    ]

    operations = [
        migrations.AddField(
            model_name="registerpostklaim",
            name="tanggal_final",
            field=models.DateField(blank=True, null=True),
        ),
    ]
