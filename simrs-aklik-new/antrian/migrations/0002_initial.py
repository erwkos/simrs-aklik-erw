# Generated by Django 3.2.12 on 2023-05-26 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('antrian', '0001_initial'),
        ('pasien', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='loket',
            name='petugas_admisi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loket_petugas_admisi', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='antrian',
            name='loket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='antrian.loket'),
        ),
        migrations.AddField(
            model_name='antrian',
            name='resume_medis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pasien.resumemedis'),
        ),
    ]
