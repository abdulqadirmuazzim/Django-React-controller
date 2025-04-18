# Generated by Django 5.1.1 on 2024-10-05 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Room",
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
                ("code", models.CharField(max_length=8, unique=True)),
                ("host", models.CharField(max_length=50, unique=True)),
                ("guest_pause", models.BooleanField(default=False)),
                ("votes_skip", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
