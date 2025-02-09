# Generated by Django 5.1.4 on 2024-12-23 10:24

import ai.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai", "0008_alter_session_created_at_delete_knowledgebase"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="client_ip",
            field=models.CharField(default="0.0.0.0", max_length=50),
        ),
        migrations.AddField(
            model_name="session",
            name="expired_at",
            field=models.DateTimeField(default=ai.models.default_expiration_time),
        ),
        migrations.AddField(
            model_name="session",
            name="location_city",
            field=models.CharField(default="Unknown City", max_length=100),
        ),
        migrations.AddField(
            model_name="session",
            name="location_country",
            field=models.CharField(default="Unknown Country", max_length=100),
        ),
        migrations.AddField(
            model_name="session",
            name="location_lat",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="session",
            name="location_lon",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="session",
            name="location_region",
            field=models.CharField(default="Unknown Region", max_length=100),
        ),
        migrations.AddField(
            model_name="session",
            name="user_agent",
            field=models.TextField(default="Unknown User Agent"),
        ),
        migrations.AlterField(
            model_name="session",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="session",
            name="session_data",
            field=models.TextField(default='{"message_history": []}'),
        ),
        migrations.AlterField(
            model_name="session",
            name="session_id",
            field=models.CharField(
                default="default_session_id", max_length=255, unique=True
            ),
        ),
    ]
