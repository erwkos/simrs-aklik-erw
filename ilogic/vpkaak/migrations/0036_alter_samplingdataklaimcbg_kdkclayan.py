# Generated by Django 4.2.5 on 2024-06-23 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpkaak", "0035_alter_samplingdataklaimcbg_kdkclayan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="samplingdataklaimcbg",
            name="Kdkclayan",
            field=models.TextField(max_length=255),
        ),
    ]
