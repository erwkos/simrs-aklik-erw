# Generated by Django 3.2.12 on 2023-05-27 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radiologi', '0003_layananradiologipasien_diagnosa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layananradiologipasien',
            name='deskripsi',
        ),
    ]
