# Generated by Django 4.2.5 on 2023-09-23 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0036_registerklaim_password_file_excel"),
    ]

    operations = [
        migrations.RemoveField(model_name="registerklaim", name="password_file_excel",),
    ]