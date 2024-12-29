# Generated by Django 5.1.4 on 2024-12-23 07:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai", "0006_alter_session_created_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="knowledgebase",
            name="label",
        ),
        migrations.AlterField(
            model_name="session",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 12, 23, 7, 17, 22, 243578, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
