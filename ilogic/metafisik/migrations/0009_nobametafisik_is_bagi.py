# Generated by Django 4.2.5 on 2024-09-14 04:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metafisik", "0008_rename_biayars_dataklaimcbgmetafisik_bytagsep_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="nobametafisik",
            name="is_bagi",
            field=models.BooleanField(default=False),
        ),
    ]