# Generated by Django 4.2.5 on 2024-07-02 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpkaak", "0040_alter_samplingdataklaimcbg_deskripsisp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="deskripsisd",
            field=models.CharField(blank=True, default="-", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="deskripsisi",
            field=models.CharField(blank=True, default="-", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="deskripsisp",
            field=models.CharField(blank=True, default="-", max_length=255, null=True),
        ),
    ]