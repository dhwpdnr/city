from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")
    default_code = "invalid"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        if isinstance(detail, tuple):
            detail = " ".join(map(str, detail))
        elif isinstance(detail, dict):
            detail = {
                k: str(v) if not isinstance(v, bool) else v for k, v in detail.items()
            }
        elif isinstance(detail, list):
            detail = " ".join(map(str, detail))
        else:
            detail = str(detail)
        self.detail = detail


class CustomAuthorizationError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Invalid input.")
    default_code = "invalid"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        if isinstance(detail, tuple):
            detail = " ".join(map(str, detail))
        elif isinstance(detail, dict):
            detail = {
                k: str(v) if not isinstance(v, bool) else v for k, v in detail.items()
            }
        elif isinstance(detail, list):
            detail = " ".join(map(str, detail))
        else:
            detail = str(detail)
        self.detail = detail
