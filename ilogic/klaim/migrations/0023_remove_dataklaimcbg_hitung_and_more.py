# Generated by Django 4.2.2 on 2023-07-23 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0022_remove_dataklaimcbg_flaghitung_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="dataklaimcbg", name="hitung",),
        migrations.RemoveField(model_name="dataklaimcbg", name="tglhitung",),
    ]
