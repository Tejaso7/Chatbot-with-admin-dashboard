# Generated by Django 5.1.4 on 2024-12-23 05:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai", "0004_sessiondata_delete_customsessionstore"),
    ]

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_id", models.CharField(max_length=255, unique=True)),
                ("session_data", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_valid", models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name="SessionData",
        ),
    ]
