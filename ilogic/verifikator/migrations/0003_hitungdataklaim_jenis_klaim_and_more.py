# Generated by Django 4.2.2 on 2023-07-23 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("verifikator", "0002_remove_hitungdataklaim_jenis_klaim_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hitungdataklaim",
            name="jenis_klaim",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="hitungdataklaim",
            name="nomor_register_klaim",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
