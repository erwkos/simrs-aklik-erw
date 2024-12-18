# Generated by Django 4.2.5 on 2024-06-17 01:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpkaak", "0025_remove_samplingdataklaimcbg_diagsekunder_koreksi_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Diagsekunder_koreksi",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Kddiagprimer_koreksi",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Nmdiagprimer_koreksi",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Nminacbgs_koreksi",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Procedure_koreksi",
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="kdsa_koreksi",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="kdsd_koreksi",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="kdsi_koreksi",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="kdsp_koreksi",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="kdsr_koreksi",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
