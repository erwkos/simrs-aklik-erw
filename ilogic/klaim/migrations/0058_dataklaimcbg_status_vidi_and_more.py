# Generated by Django 4.2.5 on 2024-08-15 04:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("klaim", "0057_dataklaimcbg_status_sinkron_dataklaimcbg_tgl_sinkron"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataklaimcbg",
            name="status_vidi",
            field=models.CharField(
                choices=[
                    ("Tidak Sinkron", "Tidak Sinkron"),
                    ("Pembahasan", "Pembahasan"),
                    ("Tidak Layak", "Tidak Layak"),
                    ("Layak", "Layak"),
                    ("Pending", "Pending"),
                    ("Dispute", "Dispute"),
                    ("Klaim", "Klaim"),
                    ("Belum Ver", "Belum Ver"),
                    ("Proses", "Proses"),
                ],
                default="Tidak Disinkron",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dataklaimcbg",
            name="status_sinkron",
            field=models.CharField(
                choices=[("Tidak Sinkron", "Tidak Sinkron"), ("Sinkron", "Sinkron")],
                default="Tidak Disinkron",
                max_length=200,
            ),
        ),
    ]