# Generated by Django 4.2.2 on 2023-07-08 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0017_rename_dataklaim_dataklaimcbg"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataklaimcbg",
            name="register",
            field=models.CharField(default=2, max_length=20),
            preserve_default=False,
        ),
    ]
