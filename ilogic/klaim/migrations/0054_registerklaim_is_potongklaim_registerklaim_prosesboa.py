# Generated by Django 4.2.5 on 2024-02-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0053_alter_jawabanpendingdispute_ket_jawaban_pending_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="registerklaim",
            name="is_potongklaim",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="registerklaim",
            name="prosesboa",
            field=models.BooleanField(default=False),
        ),
    ]
