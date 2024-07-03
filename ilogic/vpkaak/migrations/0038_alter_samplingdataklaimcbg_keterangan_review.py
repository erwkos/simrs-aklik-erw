# Generated by Django 4.2.5 on 2024-07-01 06:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpkaak", "0037_alter_samplingdataklaimcbg_kdkclayan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="keterangan_review",
            field=models.CharField(
                blank=True,
                max_length=1000,
                null=True,
                validators=[django.core.validators.MinLengthValidator(10)],
            ),
        ),
    ]
