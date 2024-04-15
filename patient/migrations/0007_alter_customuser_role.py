# Generated by Django 5.0.1 on 2024-02-28 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0006_remove_patient_role_customuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("patient", "Patient"),
                    ("donor", "Donor"),
                    ("admin", "Blood"),
                ],
                default="patient",
                max_length=10,
            ),
        ),
    ]
