# Generated by Django 4.2.2 on 2023-06-27 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('klaim', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registerklaim',
            name='verifikator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
