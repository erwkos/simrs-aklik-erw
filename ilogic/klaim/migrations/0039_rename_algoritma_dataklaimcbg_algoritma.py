# Generated by Django 4.2.5 on 2023-10-18 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0038_alter_dataklaimcbg_algoritma"),
    ]

    operations = [
        migrations.RenameField(
            model_name="dataklaimcbg", old_name="Algoritma", new_name="ALGORITMA",
        ),
    ]
