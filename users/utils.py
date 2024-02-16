import jwt, re, os
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import random
import string
from .models import User, Jwt
from utils.exceptions import CustomValidationError, CustomAuthorizationError


def get_random(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(days=365), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def decodeJWT(bearer):
    if not bearer:
        return None

    token = bearer[7:]
    try:
        decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms="HS256")
    except jwt.exceptions.ExpiredSignatureError:
        raise CustomValidationError({"data": "토큰이 만료되었습니다."})
    if decoded:
        try:
            return User.objects.get(id=decoded["user_id"])
        except User.DoesNotExist:
            return None
