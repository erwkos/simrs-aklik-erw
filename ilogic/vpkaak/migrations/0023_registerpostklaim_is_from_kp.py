# Generated by Django 4.2.5 on 2024-06-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vpkaak", "0022_remove_registerpostklaim_is_from_kp_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="registerpostklaim",
            name="is_from_kp",
            field=models.BooleanField(default=False),
        ),
    ]