# Generated by Django 4.2.5 on 2024-04-27 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vpkaak", "0009_samplingdataklaimcbg_klsrawat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="Diagsekunder",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="Procedure",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
