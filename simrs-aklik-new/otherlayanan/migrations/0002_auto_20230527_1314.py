# Generated by Django 3.2.12 on 2023-05-27 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otherlayanan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layanankonsultasipasien',
            name='deskripsi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='layananmonitoringpasien',
            name='deskripsi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='layanantindakanpasien',
            name='deskripsi',
            field=models.TextField(blank=True, null=True),
        ),
    ]
