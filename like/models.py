from django.db import models
from common.models import CommonModel


class Like(CommonModel):
    """Like Product Model Definition"""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="like_diarys"
    )
    diary = models.ForeignKey(
        "diary.Diary", on_delete=models.CASCADE, related_name="likes"
    )

    class Meta:
        unique_together = ("user", "diary")

    def __str__(self):
        return f"좋아요({self.user.username} - {self.diary.title})"
