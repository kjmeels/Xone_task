# Generated by Django 5.0.1 on 2024-04-15 17:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="age",
        ),
        migrations.RemoveField(
            model_name="user",
            name="birth_date",
        ),
        migrations.RemoveField(
            model_name="user",
            name="full_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="gender",
        ),
        migrations.RemoveField(
            model_name="user",
            name="image",
        ),
    ]
