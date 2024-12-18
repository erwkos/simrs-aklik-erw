# Generated by Django 4.2.5 on 2024-06-17 01:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpkaak", "0024_samplingdataklaimcbg_diagsekunder_koreksi_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="Diagsekunder_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="Kddiagprimer_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="Nmdiagprimer_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="Procedure_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="kdsa_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="kdsd_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="kdsi_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="kdsp_koreksi",
        ),
        migrations.RemoveField(
            model_name="samplingdataklaimcbg",
            name="kdsr_koreksi",
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Jkpst",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Kelasrsmenkes",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="Kodersmenkes",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="beratbayi",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="is_bayi",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="samplingdataklaimcbg",
            name="tanggallahirbayi",
            field=models.DateField(blank=True, null=True),
        ),
    ]
