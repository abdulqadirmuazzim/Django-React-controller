# Generated by Django 5.1.2 on 2025-03-06 23:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("track", "0002_alter_room_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="current_song",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
