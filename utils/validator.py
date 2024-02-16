from .exceptions import CustomValidationError
from users.models import User


class UsernameValidator:
    def __call__(self, value):
        if User.objects.filter(username=value).exists():
            raise CustomValidationError({"data": "이미 등록된 닉네임 입니다."})
