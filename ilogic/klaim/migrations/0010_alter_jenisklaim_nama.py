# Generated by Django 4.2.2 on 2023-07-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klaim", "0009_alter_jenisklaim_nama"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jenisklaim",
            name="nama",
            field=models.CharField(
                choices=[
                    ("CBG-Reguler", "CBG-Reguler"),
                    ("CBG-Susulan-Pending-Dispute", "CBG-Susulan-Pending-Dispute"),
                    ("Obat-Reguler", "Obat-Reguler"),
                    ("Obat-Susulan-Pending-Dispute", "Obat-Susulan-Pending-Dispute"),
                    ("Optik", "Optik"),
                    ("CAPD", "CAPD"),
                    ("Ambulance-FKRTL", "Ambulance-FKRTL"),
                    ("Alkes", "Alkes"),
                ],
                max_length=250,
            ),
        ),
    ]
