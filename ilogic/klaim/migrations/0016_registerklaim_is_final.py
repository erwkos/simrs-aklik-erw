# Generated by Django 4.2.2 on 2023-07-07 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0015_alter_registerklaim_tgl_ba_lengkap_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="registerklaim",
            name="is_final",
            field=models.BooleanField(default=False),
        ),
    ]
