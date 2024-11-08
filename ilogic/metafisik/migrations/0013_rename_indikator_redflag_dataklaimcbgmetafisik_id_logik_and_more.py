# Generated by Django 4.2.5 on 2024-09-16 03:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metafisik", "0012_rename_politusjp_dataklaimcbgmetafisik_politujsep"),
    ]

    operations = [
        migrations.RenameField(
            model_name="dataklaimcbgmetafisik",
            old_name="indikator_redflag",
            new_name="id_logik",
        ),
        migrations.AddField(
            model_name="dataklaimcbgmetafisik",
            name="indikator",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="dataklaimcbgmetafisik",
            name="keterangan_aksi",
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name="dataklaimcbgmetafisik",
            name="deskripsi_redflag",
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
