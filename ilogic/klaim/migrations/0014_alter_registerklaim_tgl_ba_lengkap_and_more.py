# Generated by Django 4.2.2 on 2023-07-02 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0013_alter_registerklaim_tgl_aju"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registerklaim",
            name="tgl_ba_lengkap",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="registerklaim",
            name="tgl_ba_verif",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="registerklaim",
            name="tgl_terima",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
