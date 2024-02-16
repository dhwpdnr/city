# Generated by Django 3.2 on 2024-02-15 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("plant", "0004_auto_20240214_2027"),
        ("diary", "0002_auto_20240214_0840"),
    ]

    operations = [
        migrations.AddField(
            model_name="diary",
            name="is_open",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="diary",
            name="location",
            field=models.CharField(
                choices=[("옥상", "옥상"), ("베란다", "베란다")],
                default="베란다",
                help_text="장소",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="DiaryPlant",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "diary",
                    models.ForeignKey(
                        help_text="일지",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diary_plants",
                        to="diary.diary",
                    ),
                ),
                (
                    "plant",
                    models.ForeignKey(
                        help_text="식물",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diary_plants",
                        to="plant.plant",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]