from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from rest_framework.views import exception_handler
from rest_framework.response import Response


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        from users.utils import decodeJWT

        user = decodeJWT(request.META.get("HTTP_AUTHORIZATION", None))
        if not user:
            return False
        request.user = user
        if request.user and request.user.is_authenticated:
            from users.models import User

            User.objects.filter(id=request.user.id).update(last_login=timezone.now())
            return True
        return False
