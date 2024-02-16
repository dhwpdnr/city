from rest_framework import serializers
from utils.exceptions import CustomValidationError
from .models import User
from utils.validator import UsernameValidator


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    def validate(self, data):
        if User.objects.filter(username=data["username"]):
            raise CustomValidationError({"data": "중복된 닉네임 입니다."})
        if data["password"] != data["password2"]:
            raise CustomValidationError({"data": "비밀번호가 일치하지 않습니다."})
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[UsernameValidator()])
