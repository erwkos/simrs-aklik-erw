# Generated by Django 4.2.2 on 2023-06-27 02:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('klaim', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerklaim',
            name='verifikator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
