# Generated by Django 4.2.2 on 2023-08-19 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0026_jawabanpendingdispute_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataklaimcbg",
            name="ket_jawaban_pending",
            field=models.ManyToManyField(to="klaim.jawabanpendingdispute"),
        ),
        migrations.AlterField(
            model_name="dataklaimcbg",
            name="ket_pending_dispute",
            field=models.ManyToManyField(to="klaim.keteranganpendingdispute"),
        ),
    ]