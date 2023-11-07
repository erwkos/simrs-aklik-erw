# Generated by Django 4.2.5 on 2023-11-04 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("faskes", "0005_alter_faskes_user_alter_kantorcabang_user"),
        ("klaim", "0046_alter_sla_kantor_cabang"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sla",
            name="kantor_cabang",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="faskes.kantorcabang",
            ),
        ),
    ]
