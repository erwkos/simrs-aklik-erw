# Generated by Django 4.2.5 on 2024-08-19 03:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("klaim", "0059_alter_dataklaimcbg_status_sinkron_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataklaimcbg",
            name="status_sinkron",
            field=models.CharField(
                choices=[
                    ("Tidak Disinkron", "Tidak Disinkron"),
                    ("Tidak Sinkron", "Tidak Sinkron"),
                    ("Sinkron", "Sinkron"),
                ],
                default="Tidak Disinkron",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="dataklaimcbg",
            name="status_vidi",
            field=models.CharField(
                choices=[
                    ("Tidak Disinkron", "Tidak Disinkron"),
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
    ]
