# Generated by Django 4.2.2 on 2023-07-21 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("klaim", "0022_remove_dataklaimcbg_flaghitung_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HitungDataKlaim",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tglhitung", models.DateTimeField(auto_now_add=True)),
                (
                    "periodehitung",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "jenis_klaim",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="klaim.jenisklaim",
                    ),
                ),
                (
                    "verifikator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
