# Generated by Django 5.1.4 on 2024-12-23 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai", "0007_remove_knowledgebase_label_alter_session_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="session",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 12, 23, 10, 0, 18, 43824, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.DeleteModel(
            name="KnowledgeBase",
        ),
    ]
