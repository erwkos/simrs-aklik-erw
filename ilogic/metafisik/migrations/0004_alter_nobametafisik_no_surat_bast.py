# Generated by Django 4.2.5 on 2024-09-08 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metafisik", "0003_dataklaimcbgmetafisik_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nobametafisik",
            name="no_surat_bast",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
