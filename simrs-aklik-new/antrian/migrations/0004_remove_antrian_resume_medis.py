# Generated by Django 3.2.12 on 2023-05-27 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('antrian', '0003_remove_antrian_no_rekam_medis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='antrian',
            name='resume_medis',
        ),
    ]
