# Generated by Django 4.2.17 on 2025-01-12 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                default="/assets/avatar.png", null=True, upload_to=""
            ),
        ),
    ]
