# Generated by Django 4.2.5 on 2024-09-16 05:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("klaim", "0062_dataklaimcbg_indikator_metafisik"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataklaimcbg",
            name="id_metafisik",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="dataklaimcbg",
            name="keterangan_aksi",
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
