# Generated by Django 5.1.2 on 2024-10-29 00:07

import track.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("track", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="code",
            field=models.CharField(
                default=track.models.generate_code, max_length=8, unique=True
            ),
        ),
    ]