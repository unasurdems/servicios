from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class UserDoesnotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'message': _('Authentication credentials were not provided.'),
        'type': 'error',
        'status': status_code
    }
    default_code = 'not_authenticated'


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {
        'message': _('Resource not found'),
        'type': 'error',
        'status': status_code
    }
    default_code = 'not found'


class PermissionDenied(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = {
        'message': _('You do not permission fot do that'),
        'type': 'error',
        'status': status_code
    }
    default_code = 'permission_denied'

    def __init__(self, message: str):
        """Personalizacion de mensaje"""
        if message:
            self.default_detail['message'] = message
        super().__init__()