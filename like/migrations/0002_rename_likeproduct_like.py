# Generated by Django 3.2 on 2024-02-15 20:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("diary", "0004_diary_farm_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("like", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="LikeProduct",
            new_name="Like",
        ),
    ]