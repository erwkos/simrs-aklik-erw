# Generated by Django 4.2.2 on 2023-07-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0021_rename_ket_pending_dataklaimcbg_ket_pending_dispute"),
    ]

    operations = [
        migrations.RemoveField(model_name="dataklaimcbg", name="flaghitung",),
        migrations.AddField(
            model_name="dataklaimcbg",
            name="is_hitung",
            field=models.BooleanField(default=False),
        ),
    ]
