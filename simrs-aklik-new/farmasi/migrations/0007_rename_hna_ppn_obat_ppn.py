# Generated by Django 3.2.12 on 2023-05-30 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmasi', '0006_alter_obat_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='obat',
            old_name='hna_ppn',
            new_name='ppn',
        ),
    ]
