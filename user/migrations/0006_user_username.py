# Generated by Django 4.2.4 on 2023-08-27 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_remove_follow_following_follow_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=63, null=True, unique=True),
        ),
    ]
