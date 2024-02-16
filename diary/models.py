from django.db import models
from common.models import CommonModel


class Diary(CommonModel):
    """Diary Model Definition"""

    class TypeChoices(models.TextChoices):
        plant = ("농업일지", "농업일지")
        farm = ("밭자랑", "밭자랑")

    class LocationChoices(models.TextChoices):
        roof = ("옥상", "옥상")
        veranda = ("베란다", "베란다")

    title = models.CharField(max_length=100, help_text="제목")
    description = models.TextField(help_text="본문")
    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices,
        default=TypeChoices.plant,
        help_text="일지 타입",
    )
    location = models.CharField(
        max_length=20,
        choices=LocationChoices.choices,
        default=LocationChoices.veranda,
        help_text="장소",
    )
    user = models.ForeignKey(
        "users.User",
        related_name="diaries",
        on_delete=models.SET_NULL,
        null=True,
        help_text="작성자",
    )
    farm_image = models.TextField(
        blank=True, null=True, default="", help_text="밭 자랑 이미지"
    )
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.id}) {self.title} - {self.user.username if self.user else ''}"


class DairyImage(CommonModel):
    """DairyImage Model Definition"""

    diary = models.ForeignKey(
        "diary.Diary", related_name="images", on_delete=models.CASCADE, help_text="일지"
    )
    path = models.TextField(help_text="저장 경로")

    def __str__(self):
        return f"{self.diary.title} - sub image {self.path} ({self.id})"


class DiaryPlant(CommonModel):
    """DiaryPlant Model Definition"""

    diary = models.ForeignKey(
        "diary.Diary",
        related_name="diary_plants",
        on_delete=models.CASCADE,
        help_text="일지",
    )
    plant = models.ForeignKey(
        "plant.Plant",
        related_name="diary_plants",
        on_delete=models.CASCADE,
        help_text="식물",
    )

    def __str__(self):
        return f"{self.diary.title} -  {self.plant.nickname} ({self.id})"
