# Generated by Django 4.2.2 on 2023-06-29 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_block_login_time_user_login_attempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blocked_count',
            field=models.IntegerField(default=0),
        ),
    ]