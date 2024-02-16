from django.db import models
from common.models import CommonModel


class Comment(CommonModel):
    """Comment Model Definition"""

    diary = models.ForeignKey(
        "diary.Diary",
        related_name="comments",
        on_delete=models.CASCADE,
        help_text="일지",
    )
    user = models.ForeignKey(
        "users.User",
        related_name="comments",
        on_delete=models.CASCADE,
        help_text="일지",
    )
    description = models.TextField()

    def __str__(self):
        return f"({self.id}) {self.diary.title}의 {self.user.username} 댓글"
