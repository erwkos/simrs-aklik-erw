# Generated by Django 3.2.12 on 2023-05-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasien', '0003_auto_20230527_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendaftaran',
            name='status_layanan',
            field=models.CharField(blank=True, choices=[('Berlangsung', 'Berlangsung'), ('Selesai', 'Selesai')], default='Berlangsung', max_length=100, null=True),
        ),
    ]
